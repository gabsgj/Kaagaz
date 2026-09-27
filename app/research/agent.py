"""
Kaagaz — the research agent.

One function, `answer()`, is the whole product:

    request -> cache lookup -> (hit: return dated answer)
                            -> (miss/stale: search -> synthesise -> store -> return)

It is also the only place that decides what to do when a step fails. The rules,
in priority order:

  1. A fresh cache hit is returned immediately. No network, no latency.
  2. A stale entry with usable content is returned *labelled stale* if the
     refresh fails — an out-of-date answer with a visible "as of" date is far
     more useful to someone about to visit a bank than an error page.
  3. Search failure -> try synthesis over nothing? No. Return a typed failure
     the UI can render as a real message.
  4. Synthesis failure -> fall back to presenting the raw search findings as
     prose with sources attached. The user gets a real, sourced answer even
     when the structuring step is down.
"""

import time
from datetime import datetime, timezone

from . import cache as cache_mod
from . import refdata
from .search import search, SearchError, build_research_query
from .synthesize import synthesize, REGULATORY_LABELS


class ResearchFailed(Exception):
    """Typed failure the UI renders as a specific, non-blank message.

    ``suggestions`` carries links to cached cases that overlap the request, so
    a dead end becomes "here is what we do know" rather than a blank error.
    """

    def __init__(self, message, kind="search", retryable=True, suggestions=None):
        super().__init__(message)
        self.message = message
        self.kind = kind
        self.retryable = retryable
        self.suggestions = suggestions or []


def _now_iso():
    return datetime.now(timezone.utc).isoformat()


def _similar_entries(app, req, limit=4):
    """Cached cases that overlap a request we could not research.

    Live search being down should never be a dead end. This ranks the
    pre-researched cases by how much they share with the request — same
    transaction type first, then same bank — and returns links, so the failure
    screen can say "we could not research that, but here is what we do know".
    """
    try:
        entries = cache_mod.list_entries(app, limit=200)
    except Exception:
        return []
    tx = (req.get("transaction_type") or "").strip().lower()
    bank = (req.get("bank") or "").strip().lower()
    # Callers pass a parsed request containing both the canonical residency
    # code (`residency`) and a long search phrase (`residency_phrase`). The
    # cache stores the code, so match the code; otherwise a long English phrase
    # never equals `resident` and every overlapping suggestion is lost.
    residency_raw = (req.get("residency") or "").strip().lower()
    if residency_raw in refdata.RESIDENCY:
        residency = residency_raw
    else:
        # A worker may receive an unparsed request whose residency is a phrase
        # rather than a code. Match only exact known phrases; never let an
        # unknown value silently become `resident` and earn a false point.
        phrase = (req.get("residency_phrase") or "").strip().lower()
        residency = {
            value.lower(): key
            for key, value in refdata.RESIDENCY_PHRASES.items()
        }.get(phrase, "")

    scored = []
    for e in entries:
        # The cache stores the transaction type under
        # `loan_or_transaction_type` and residency under
        # `applicant_residency_status`; older code reaching for
        # `transaction_type`/`residency` got nothing and returned an empty
        # suggestion list on exactly the failure path this exists to fix.
        etx = (e.get("loan_or_transaction_type") or "").strip().lower()
        ebank = (e.get("bank") or "").strip().lower()
        eres = (e.get("applicant_residency_status") or "").strip().lower()
        score = 0
        if tx and etx and (tx == etx or tx in etx or etx in tx):
            score += 4
        if bank and ebank and (bank == ebank or bank in ebank or ebank in bank):
            score += 2
        if residency and eres and residency == eres:
            score += 1
        if score:
            scored.append((score, e))
    scored.sort(key=lambda pair: (-pair[0], pair[1].get("loan_or_transaction_type") or ""))

    out = []
    for score, e in scored[:limit]:
        tx = e.get("loan_or_transaction_type") or ""
        bank = e.get("bank") or ""
        residency = e.get("applicant_residency_status") or ""
        state = e.get("state") or ""
        out.append({
            "transaction_type": tx,
            "bank": bank,
            "residency": residency,
            "state": state,
            "label": _label_for(tx, bank, residency),
            "href": _href_for(tx, bank, residency, state),
        })
    return out


def _label_for(tx, bank, residency):
    parts = [tx or "Document checklist"]
    if bank:
        parts.append(bank)
    if residency and residency != "not_applicable":
        parts.append(residency.replace("_", " "))
    return " · ".join(p for p in parts if p)


def _href_for(tx, bank, residency, state):
    """Build the checklist URL by hand.

    `url_for` needs an application context, and this runs inside a background
    worker thread where there is none — the first version raised
    "Working outside of application context" on exactly the failure path this
    code exists to serve. The route is a fixed shape, so build it directly.
    """
    from urllib.parse import quote
    parts = [
        "transaction_type=" + quote(tx or ""),
        "bank=" + quote(bank or ""),
        "residency=" + quote(residency or ""),
    ]
    if state:
        parts.append("state=" + quote(state))
    return "/checklist?" + "&".join(parts)


def _as_of(entry):
    raw = entry.get("researched_at")
    try:
        dt = datetime.fromisoformat(raw)
    except (TypeError, ValueError):
        return "an earlier date"
    # strftime("%-d") is a glibc extension and is not portable to macOS.
    return "%d %s %d" % (dt.day, dt.strftime("%B"), dt.year)


def parse_request(form):
    """Normalise a raw user request into a canonical one.

    Nothing here rejects a value. Unknown banks, unknown products and unknown
    states all pass straight through — they are exactly the cases the live
    research step exists to handle.
    """
    transaction = refdata.normalize_category(form.get("transaction_type", ""))
    bank = refdata.normalize_bank(form.get("bank", ""))
    state = refdata.normalize_state(form.get("state", ""))
    residency = refdata.normalize_residency(form.get("residency", ""))

    # A transaction is the one field we genuinely cannot proceed without.
    if not transaction:
        raise ResearchFailed(
            "Tell us what you're trying to do — for example “home loan” or "
            "“loan against FD”.",
            kind="invalid_request", retryable=False,
        )

    # Some transactions cannot vary by residency — registering a sale deed in
    # Kerala is the same checklist whether you live in Kochi or Chicago. Asking
    # again under a different residency would research an identical question and
    # file it as a second cache entry, so we canonicalise it. An *explicit*
    # residency choice is still honoured, in case the bank genuinely does treat
    # them differently.
    explicit = (form.get("residency") or "").strip().lower()
    if (transaction.lower() in refdata.RESIDENCY_IRRELEVANT
            and explicit in ("", "resident", "not_applicable")):
        residency = "not_applicable"

    return {
        "transaction_type": transaction,
        "bank": bank,
        "state": state,
        "residency": residency,
        "residency_label": refdata.residency_label(residency),
        "residency_phrase": refdata.residency_phrase(residency),
        "residency_blurb": refdata.RESIDENCY.get(residency, {}).get("blurb", ""),
    }


def _decorate(request, answer, entry):
    """Attach presentation metadata the templates need."""
    return {
        "request": request,
        "answer": answer,
        "items": answer.get("items", []),
        "total": len(answer.get("items", [])),
        "sources": answer.get("sources", []) or entry.get("source_urls", []),
        "researched_at": entry.get("researched_at", ""),
        "as_of": _as_of(entry),
        "research_query": entry.get("research_query", ""),
        "search_query": entry.get("search_query", ""),
        "model": entry.get("model", ""),
        "provider": entry.get("provider", ""),
        "is_seed": entry.get("is_seed", False),
        "stale": bool(entry.get("stale")),
        "age_days": entry.get("age_days"),
        "ttl_days": entry.get("cache_ttl_days"),
    }


def answer(app, request_dict, on_stage=None, force_refresh=False):
    """Cache-first, research-on-miss. The main entry point.

    `on_stage(label, detail)` streams progress for the flip-board UI.
    """
    req = parse_request(request_dict)
    cache_key = cache_mod.make_cache_key(
        req["transaction_type"], req["bank"], req["residency"], req["state"]
    )
    req["cache_key"] = cache_key

    # ── 1. Cache check ──────────────────────────────────────────────────────
    if not force_refresh:
        hit = cache_mod.get_fresh(app, cache_key)
        if hit:
            cache_mod.touch(app, cache_key)
            payload = _decorate(req, hit["answer"], hit)
            payload["cache"] = "hit"
            payload["latency_ms"] = 0
            if on_stage:
                try:
                    on_stage("Served from cache", f"as of {payload['as_of']}")
                except Exception:
                    pass
            return payload

    # ── 2. Live research ────────────────────────────────────────────────────
    t0 = time.monotonic()

    if on_stage:
        try:
            on_stage("Checking sources", req["transaction_type"])
        except Exception:
            pass

    try:
        found = search(
            req["transaction_type"], req["bank"], req["residency_phrase"],
            req["state"], on_stage=on_stage,
        )
    except SearchError as exc:
        # Search is down. A stale-but-real answer beats a dead end.
        stale = cache_mod.get_any(app, cache_key)
        if stale:
            payload = _decorate(req, stale["answer"], stale)
            payload["cache"] = "stale"
            payload["stale"] = True
            payload["age_days"] = round(
                (time.time() - stale["researched_at_epoch"]) / 86400.0, 1
            )
            payload["degraded"] = (
                "Live research is unavailable right now, so this is the last "
                f"researched answer ({payload['as_of']})."
            )
            return payload
        raise ResearchFailed(
            "We couldn't reach the research service just now. "
            "Please try again in a moment.",
            kind="search_unavailable",
            suggestions=_similar_entries(app, req),
        ) from exc

    # ── 3. Synthesis ────────────────────────────────────────────────────────
    if on_stage:
        try:
            on_stage("Building your checklist", f"{len(found['citations'])} sources")
        except Exception:
            pass

    citation_urls = [c["url"] for c in found["citations"] if c.get("url")]
    syn = synthesize(
        req["transaction_type"], req["bank"], req["residency_phrase"],
        req["state"], found["findings"], found["citations"],
    )

    degraded_note = ""
    answer_obj = syn.get("answer")
    if answer_obj is None:
        # 4. Degrade to a prose answer built from the search findings. Still
        # real, still sourced — just not structured.
        answer_obj = _prose_answer(found)
        degraded_note = (
            "The checklist could not be structured automatically, so this is the "
            "raw researched answer with its sources."
        )

    # ── 4. Store — the row is both cache and audit trail ────────────────────
    latency = int((time.monotonic() - t0) * 1000)
    if on_stage:
        try:
            on_stage("Saving to the record", f"{len(answer_obj['items'])} steps")
        except Exception:
            pass

    entry = cache_mod.store(
        app,
        cache_key,
        transaction_type=req["transaction_type"],
        bank=req["bank"],
        residency=req["residency"],
        state=req["state"],
        answer=answer_obj,
        source_urls=citation_urls,
        research_query=found["query"],
        search_query=build_research_query(
            req["transaction_type"], req["bank"], req["residency_phrase"],
            req["state"]
        ),
        summary=answer_obj.get("summary", ""),
        interest_rate_range=answer_obj.get("interest_rate_range", ""),
        processing_fee_note=answer_obj.get("processing_fee_note", ""),
        regulatory_note=answer_obj.get("regulatory_note", ""),
        model=found["model"],
        provider=syn.get("provider", ""),
        latency_ms=latency,
        ttl_days=cache_mod.DEFAULT_TTL_DAYS,
    )

    payload = _decorate(req, answer_obj, entry)
    payload["cache"] = "miss"
    payload["latency_ms"] = latency
    if degraded_note:
        payload["degraded"] = degraded_note
    return payload


def _prose_answer(found):
    """Fallback shape when synthesis fails — keep the real content, drop the JSON.

    One item holds the whole findings text so the user still gets the answer
    and the sources, just without the per-step cost/time breakdown.
    """
    text = found["findings"]
    body = text if len(text) <= 4000 else text[:4000].rsplit("\n", 1)[0] + " …"
    return {
        "summary": body[:1200],
        "items": [
            {
                "step_order": 1,
                "document_name": "Full researched answer",
                "plain_explanation": body,
                "where_to_obtain": "See the sources listed below",
                "approx_cost_min": None,
                "approx_cost_max": None,
                "approx_time_days": None,
                "regulatory_source": "bank_internal",
                "depends_on": "",
                "source_note": "Search research, unstructured",
            }
        ],
        "interest_rate_range": "",
        "processing_fee_note": "",
        "regulatory_note": "",
        "disclosures": [
            "This answer was returned unstructured because the checklist "
            "formatting step was unavailable."
        ],
        "sources": found["citations"],
    }


def research_labels():
    """Regulatory bucket metadata for the legend strip."""
    return [
        {"key": key, "label": REGULATORY_LABELS[key]} for key in REGULATORY_LABELS
    ]
