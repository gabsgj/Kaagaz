"""
Kaagaz — Step 1 of the research pipeline: the search.

This module does exactly one job: find real sources for a banking question and
hand back what they say, *plus the URLs they came from*. The URLs are not
decoration — they become the citation list on screen and the audit trail in
SQLite.

Two backends, in order of preference:

  1. **Direct search + page fetch (no API key).** DuckDuckGo's keyless endpoint
     for the result list, then fetch the pages themselves and strip them to
     text. This grounds the generation step in the *actual page content* rather
     than in another model's summary of it, which is strictly better grounding
     and gives exact control over which sources get cited.

  2. **Model-native web access** (OpenRouter ":online"). Used when the direct
     path is blocked or rate-limited. Weaker on citations and, in practice,
     dependent on a paid key.

Design note (logged in .aimem/decisions.md): this is the explicit two-step
tool-use pattern, not a ":online" suffix on the generation model. Doing search
and synthesis separately means we control which sources are cited, and it lets
the generation step keep using an independent provider chain — a search outage
does not take generation down with it.
"""

import os
import re
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from html import unescape
from urllib.parse import unquote

import requests

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

DDG_LITE_URL = "https://lite.duckduckgo.com/lite/"
DDG_HTML_URL = "https://html.duckduckgo.com/html/"

# Model-native web search, used only if the direct path fails. All are
# OpenRouter-hosted models reached through the ":online" suffix.
SEARCH_MODELS = [
    "google/gemini-2.5-flash:online",
    "openai/gpt-4o-mini:online",
    "perplexity/sonar",
]

SEARCH_TIMEOUT = 90        # seconds — a cold research call is slow by nature
PAGE_TIMEOUT = 15          # seconds per page fetch
FETCH_PAGES = 5            # how many top results to actually read
MAX_PAGE_CHARS = 6000      # per page, so one long page cannot crowd out the rest

BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
             "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

# Seconds to wait before retrying a throttled direct search.
#
# A 202/anomaly/captcha response from DuckDuckGo is a *hard* block, not a
# transient throttle: it has been observed lasting for hours from a single IP.
# Retrying it three times over 28 seconds does not clear it — it just makes the
# user stare at a spinner for half a minute before the same failure. So a
# detected block fails fast, and only a bare 429 with no challenge body (which
# can be a momentary rate limit) gets one short retry.
DIRECT_SEARCH_RETRIES = (0, 5)

# Domains that are never a useful source for this domain, and which would
# otherwise dominate a generic query with boilerplate or previews.
_SKIP_HOSTS = (
    "duckduckgo.com", "wikipedia.org", "youtube.com", "facebook.com",
    "instagram.com", "twitter.com", "x.com", "linkedin.com", "pinterest.com",
    "amazon.", "ebay.", "quora.com", "reddit.com", "glassdoor.com",
    "scribd.com", "slideshare.net", "researchgate.net", "issuu.com",
    "coursehero", "scribd", "pdfcoffee", "docslib", "studylib",
)

# Hosts that are authoritative for this problem. Used to rank, not to filter —
# a bank nobody has heard of still gets researched.
_TIER1_HOSTS = ("rbi.org.in", "indiacode.nic.in", "egazette", "nic.in",
               "gov.in", "registration.", "nta.gov", "sebi.gov.in")
_TIER2_SUFFIXES = (".bank.in", "bank.in/", "hdfcbank.com", "axisbank.com",
                   "kotak.com", "icicibank.com", "federalbankonline.com")


def _host_of(url):
    try:
        return url.split("//", 1)[-1].split("/")[0].lower().removeprefix("www.")
    except Exception:
        return ""


def _tier(hit, bank=""):
    """Rank a result: lower is better.

    This matters more than it looks. A generic web search for "home loan
    documents required" is dominated by SEO listicles and Scribd previews, and
    an earlier run of this module returned two Scribd documents and three
    aggregators with the bank's own product page ranked out of the top five.
    The answer a bank publishes about itself is worth more than any third-party
    summary of it, so it is promoted rather than merely preferred.
    """
    host = _host_of(hit["url"])
    if bank:
        bank_tokens = [t for t in bank.lower().replace(",", " ").split()
                       if len(t) > 3 and t not in ("bank", "ltd", "limited")]
        for token in bank_tokens:
            if token.replace(" ", "") in host.replace("-", "").replace(".", ""):
                return 0
    if any(t in host for t in _TIER1_HOSTS):
        return 1
    if any(s in hit["url"].lower() for s in _TIER2_SUFFIXES):
        return 2
    return 3


def _rank(hits, bank=""):
    """Stable sort by tier, keeping DuckDuckGo's own relevance order within
    each tier so we do not flatten a good ranking into alphabetical order."""
    return [h for _, _, h in sorted(
        ((_tier(h, bank), i, h) for i, h in enumerate(hits)),
        key=lambda t: (t[0], t[1]),
    )]



class SearchError(Exception):
    """Raised when no search backend could be reached."""


class _RateLimited(Exception):
    """The engine answered with an anti-bot page rather than an error."""


# DuckDuckGo serves HTTP 202 with a ~14KB challenge page once it decides a
# client is going too fast, and it does NOT look like an error. A first version
# of this module treated 202 as success, parsed zero results out of the
# challenge page, and reported "no search backend available" — which is
# technically true and completely unhelpful, because the real cause was
# throttling we caused ourselves.
_MIN_INTERVAL_BETWEEN_QUERIES = 3.0   # seconds, in-process
_last_query_at = 0.0
_query_lock = None


def _init_lock():
    global _query_lock
    if _query_lock is None:
        import threading
        _query_lock = threading.Lock()
    return _query_lock


def _throttle():
    """Space queries out so we do not trigger our own block."""
    global _last_query_at
    wait = _MIN_INTERVAL_BETWEEN_QUERIES - (time.monotonic() - _last_query_at)
    if wait > 0:
        time.sleep(wait)
    _last_query_at = time.monotonic()


def _looks_blocked(resp, body):
    if resp.status_code in (202, 429, 503):
        return True
    low = body[:4000].lower()
    return ("anomaly" in low or "captcha" in low or "unusual traffic" in low
            or "are you a robot" in low or "challenge" in low)


# ────────────────────────────────────────────────────────────────────────────
# Direct search + page fetch
# ────────────────────────────────────────────────────────────────────────────

def _clean(text):
    return " ".join((text or "").strip().split())


def _decode_url(raw):
    """DuckDuckGo wraps result URLs in a percent-encoded `uddg` parameter.

    html.unescape() is not enough and is the reason an earlier version of this
    module returned `https%3A%2F%2F...` and then failed to fetch any of them:
    every "URL" was a literal percent-encoded string, so every request 404'd.
    """
    return unquote(unescape(raw or ""))


def _strip_html(raw):
    """Readable text out of a page, with scripts and navigation removed."""
    raw = re.sub(r"(?is)<(script|style|noscript|svg|head)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?is)<!--.*?-->", " ", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", unescape(raw)).strip()


def _parse_ddg_lite(html_text):
    """Result links and titles out of DuckDuckGo's keyless HTML."""
    out, seen = [], set()
    for m in re.finditer(r'href="(//duckduckgo\.com/l/\?uddg=[^"]+)"', html_text):
        raw = m.group(1)
        target = re.search(r"uddg=([^&]+)", raw)
        if not target:
            continue
        url = _decode_url(target.group(1))
        if not url.startswith("http") or url in seen:
            continue
        seen.add(url)
        # Title sits in the anchor text just after the href.
        tail = html_text[m.end():m.end() + 400]
        title = ""
        t = re.search(r">\s*(?:<[^>]+>\s*)*([^<]{4,200})", tail)
        if t:
            title = _clean(unescape(t.group(1)))
        out.append({"url": url, "title": title})
    return out


def _parse_ddg_html(html_text):
    """Result links and titles out of DuckDuckGo's full HTML endpoint."""
    out, seen = [], set()
    for m in re.finditer(
        r'<a[^>]+class="[^"]*result__a[^"]*"[^>]+href="([^"]+)"[^>]*>(.*?)</a>',
        html_text, re.DOTALL,
    ):
        href, title_html = m.group(1), m.group(2)
        target = re.search(r"uddg=([^&]+)", href)
        url = _decode_url(target.group(1)) if target else _decode_url(href)
        if not url.startswith("http") or url in seen:
            continue
        seen.add(url)
        title = _clean(_strip_html(title_html))
        out.append({"url": url, "title": title})
    return out


def _query_once(query):
    """One query against DuckDuckGo's keyless endpoints, most reliable first.

    Raises _RateLimited rather than returning an empty list, so the caller can
    tell "this engine is throttling us" apart from "this engine has no results
    for that phrasing" and choose differently.
    """
    throttled = False
    for url, parser in ((DDG_LITE_URL, _parse_ddg_lite),
                        (DDG_HTML_URL, _parse_ddg_html)):
        try:
            with _init_lock():
                _throttle()
            resp = requests.get(url, params={"q": query},
                                headers={"User-Agent": BROWSER_UA}, timeout=20)
            if _looks_blocked(resp, resp.text):
                throttled = True
                continue
            resp.raise_for_status()
            hits = [h for h in parser(resp.text)
                    if not any(s in h["url"] for s in _SKIP_HOSTS)]
            if hits:
                return hits
        except _RateLimited:
            throttled = True
        except Exception:
            continue
    if throttled:
        raise _RateLimited("duckduckgo throttled the request")
    return []


def _results_for(query, bank=""):
    """Run the broad query, plus a second one biased at the bank's own site.

    A single generic query surfaces whatever ranks highest for that phrasing,
    which is reliably listicles. The second query is what puts the bank's own
    product page — the single most authoritative source available — into the
    candidate set. Results are merged, de-duplicated and ranked.

    The second query is skipped when the first already found an authoritative
    source, because every extra query is another chance to trip the throttle.
    """
    merged, seen = [], set()

    def absorb(hits):
        for h in hits:
            key = h["url"].rstrip("/")
            if key in seen:
                continue
            seen.add(key)
            merged.append(h)

    absorb(_query_once(query))

    # Already have the bank's own page or a regulator? Nothing to gain from
    # spending another query.
    already_authoritative = any(_tier(h, bank) <= 1 for h in merged)

    if bank and not already_authoritative:
        bank_tokens = [t for t in bank.lower().replace(",", " ").split()
                       if len(t) > 3 and t not in ("bank", "ltd", "limited")]
        if bank_tokens:
            site = " ".join(t.capitalize() for t in bank_tokens)
            try:
                absorb(_query_once("%s %s documents required" % (site, query[:80])))
            except _RateLimited:
                pass  # the broad query's results are still good enough

    return _rank(merged, bank)


def _fetch_page(hit):
    """Read one result. Never raises — a dead link just yields no text."""
    try:
        resp = requests.get(hit["url"], headers={"User-Agent": BROWSER_UA},
                            timeout=PAGE_TIMEOUT, allow_redirects=True)
        if resp.status_code >= 400:
            return None
        ctype = resp.headers.get("Content-Type", "")
        if "html" not in ctype and "text" not in ctype and "json" not in ctype:
            return None
        text = _strip_html(resp.text)
        if len(text) < 200:
            return None
        return {**hit, "text": text[:MAX_PAGE_CHARS]}
    except Exception:
        return None


def _direct_search(transaction_type, bank, residency_phrase, state, on_stage):
    """Search and read. Returns None if the direct path is unusable."""
    if on_stage:
        on_stage("Searching the web", "direct search")
    t0 = time.monotonic()

    bank_part = f" at {bank}" if bank else ""
    state_part = f" in {state}" if state else ""
    query = (f"{transaction_type}{bank_part}{state_part} documents required "
             f"list for {residency_phrase}")
    try:
        hits = _results_for(query, bank)
    except _RateLimited as exc:
        # A throttle is not a result. Let the caller decide whether a short
        # retry or the model-backed fallback comes next.
        if on_stage:
            on_stage("Direct search throttled", "switching provider")
        raise
    if not hits:
        return None

    if on_stage:
        on_stage("Reading sources", f"{len(hits)} results found")
    t1 = time.monotonic()

    with ThreadPoolExecutor(max_workers=FETCH_PAGES) as pool:
        pages = list(pool.map(_fetch_page, hits[:FETCH_PAGES]))
    pages = [p for p in pages if p]

    if not pages:
        return None

    if on_stage:
        on_stage("Building your checklist", f"{len(pages)} sources read")

    # Build the grounding text the synthesis step will read.
    parts = []
    for i, page in enumerate(pages, start=1):
        header = f"[{i}] {page['title'] or page['url']}\nSOURCE: {page['url']}\n"
        parts.append(header + page["text"])
    findings = "\n\n".join(parts)

    return {
        "findings": findings,
        "citations": [{"url": p["url"], "title": p["title"] or p["url"]}
                      for p in pages],
        "model": "duckduckgo + direct-fetch",
        "provider": "direct",
        "latency_ms": int((time.monotonic() - t0) * 1000),
        "query": query,
        "searched_at": datetime.utcnow().isoformat(),
        "search_ms": int((t1 - t0) * 1000),
        "read_ms": int((time.monotonic() - t1) * 1000),
    }



def build_research_query(transaction_type, bank, residency_phrase, state):
    """The exact research question. Stored verbatim for the audit trail."""
    bank_part = f" at {bank}" if bank else ""
    state_part = f" in {state}" if state else ""
    return (
        f"What documents, in what order, with what approximate costs and how many "
        f"working days each step takes, are required for {transaction_type}"
        f"{bank_part}{state_part} for {residency_phrase}? "
        f"Also state the current interest rate range as a band (for example "
        f"\"8.50% - 9.75% p.a.\") and the processing fee. "
        f"Note separately which items come from RBI rules, which from the state "
        f"stamp act or registrar, and which are the bank's own policy. "
        f"If a detail is not publicly disclosed, say so explicitly rather than "
        f"estimating. Cite every source."
    )


def _search_prompt(transaction_type, bank, residency_phrase, state):
    bank_part = f" at {bank}" if bank else " (any major Indian bank)"
    state_part = f", with the property/applicant situated in {state}" if state else ""
    return (
        "You are a research assistant compiling an authoritative document checklist "
        "for an Indian banking transaction. Research this on the live web and report "
        "only what you can source.\n\n"
        f"TRANSACTION: {transaction_type}{bank_part}{state_part}\n"
        f"APPLICANT: {residency_phrase}\n\n"
        "Report, in this order:\n"
        "1. The documents/steps in the sequence the applicant actually does them. "
        "Split every bundle into its individual documents — 'last 3 months' salary "
        "slips' and 'latest ITR acknowledgement' are separate items, not one 'income "
        "documents' row. An ordinary home loan has 10-18 distinct documents.\n"
        "2. For each: what it is in one line, where to get it, approximate cost in "
        "INR, and typical time in working days.\n"
        "3. Any attestation, notarisation, apostille or FEMA declaration that applies.\n"
        "4. Interest rate as a BAND (never a single number — actual rate depends on "
        "credit score, amount and tenure) and the processing fee. Open the bank's own "
        "interest-rate or product page and read the published band off it. If the page "
        "gives only a floor ('X% onwards'), say so and give the band you can justify. "
        "If no rate is published at all, write 'not publicly disclosed'.\n"
        "5. Which regulator or authority governs each group of items: RBI, the state "
        "stamp act / sub-registrar, or the bank's internal policy.\n\n"
        "Hard rules:\n"
        "- Prefer the bank's own official website, RBI circulars, and the state "
        "government's stamp-act page over aggregators and blogs. Use aggregators only "
        "as a cross-check.\n"
        "- If a bank or state does not publish a figure, write 'not publicly disclosed, "
        "contact the bank directly'. Never invent a number.\n"
        "- Never attribute stamp duty or registration fees to the RBI.\n"
        "- Cite every claim with a numbered source marker like [1]."
    )


def _extract_citations(message):
    """Collect real URLs + titles the model actually read.

    Prefers OpenRouter's structured `annotations`; falls back to scraping
    bare URLs out of the body for backends that inline them instead.
    """
    out = []
    seen = set()

    for ann in message.get("annotations") or []:
        cite = (ann or {}).get("url_citation") or {}
        url = (cite.get("url") or "").strip()
        if url and url not in seen:
            seen.add(url)
            out.append({"url": url, "title": (cite.get("title") or "").strip()})

    if not out:
        body = message.get("content") or ""
        for m in re.finditer(r"https?://[^\s\)\]\}\"'<>]+", body):
            url = m.group(0).rstrip(".,;:")
            if url not in seen:
                seen.add(url)
                out.append({"url": url, "title": ""})
    return out


def _call_openrouter_search(model, prompt, max_tokens):
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        raise ValueError("No OpenRouter API key")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://kaagaz.app",
        "X-Title": "Kaagaz Research",
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a precise web researcher. You always search before "
                    "answering and you always cite. You never state a figure you "
                    "could not find a source for."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.1,
    }
    resp = requests.post(
        OPENROUTER_API_URL, headers=headers, json=payload, timeout=SEARCH_TIMEOUT
    )
    resp.raise_for_status()
    return resp.json()


def search(transaction_type, bank="", residency_phrase="", state="",
           on_stage=None, max_tokens=1800):
    """Run the search step.

    Returns dict: {findings, citations, model, provider, latency_ms, query}

    `on_stage(stage_label, detail)` is called as the pipeline advances so the
    flip-board in the UI has something real to show. It must never raise.
    """
    query = build_research_query(transaction_type, bank, residency_phrase, state)

    def stage(label, detail=""):
        if on_stage:
            try:
                on_stage(label, detail)
            except Exception:
                pass

    errors = []

    # 1. Direct search + page fetch. No key, real page text, exact citations.
    if os.environ.get('KAAGAZ_DISABLE_DIRECT_SEARCH', '').lower() not in ('1', 'true', 'yes'):
        # DuckDuckGo throttles hard. A detected block usually persists longer than
        # a cold-research wait, so allow only one short retry before falling
        # through to the genuinely different model-backed provider.
        for attempt in range(1, len(DIRECT_SEARCH_RETRIES) + 1):
            try:
                direct = _direct_search(transaction_type, bank,
                                        residency_phrase, state, on_stage)
            except _RateLimited as exc:
                errors.append("throttled: %s" % exc)
                if attempt < len(DIRECT_SEARCH_RETRIES):
                    if on_stage:
                        on_stage("Search throttled",
                                 "retrying in %ds" % DIRECT_SEARCH_RETRIES[attempt])
                    time.sleep(DIRECT_SEARCH_RETRIES[attempt])
                continue
            except Exception as exc:  # noqa: BLE001
                errors.append("direct: %s" % exc)
                break
            else:
                if direct:
                    direct["query"] = query
                    return direct
                break  # no results is a real answer, not a reason to retry

    # 2. Model-native web access, if a paid key happens to be available.
    prompt = _search_prompt(transaction_type, bank, residency_phrase, state)
    for model in SEARCH_MODELS:
        stage("Searching the web", model)
        t0 = time.monotonic()
        try:
            data = _call_openrouter_search(model, prompt, max_tokens)
            message = data["choices"][0]["message"]
            findings = (message.get("content") or "").strip()
            if not findings:
                raise ValueError("empty response from search model")
            citations = _extract_citations(message)
            latency = int((time.monotonic() - t0) * 1000)
            stage("Reading sources", f"{len(citations)} source"
                                       f"{'s' if len(citations) != 1 else ''} found")
            return {
                "findings": findings,
                "citations": citations,
                "model": model,
                "provider": "openrouter:web",
                "latency_ms": latency,
                "query": query,
                "searched_at": datetime.utcnow().isoformat(),
            }
        except Exception as exc:  # try the next search backend
            errors.append("%s: %s" % (model, exc))
            continue

    stage("Search unavailable", "")
    raise SearchError(
        "No search backend available (%s)" % "; ".join(errors[:3])
    )
