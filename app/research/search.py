"""
Kaagaz — Step 1 of the research pipeline: the search.

This module does exactly one job: put a well-formed research question in front of
a model that has live web access, and hand back what it found *plus the URLs it
actually read*. The URLs are not decoration — they become the citation list on
screen and the audit trail in SQLite.

Design note (logged in .aimem/decisions.md): this is the explicit two-step
tool-use pattern, not a ":online" suffix on the generation model. Doing search
and synthesis separately means we control which sources get cited, and it lets
the generation step keep using the existing OpenRouter -> NVIDIA NIM fallback
chain — a model with web access is only available on OpenRouter, and we do not
want search availability to be coupled to generation availability.
"""

import os
import re
import time
from datetime import datetime

import requests

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Search-tier models, best first. All are OpenRouter-hosted models with live
# web access via the ":online" suffix, which routes the request through a
# search step and returns citations as structured `annotations`.
#
# Ordering note: this list was determined empirically against the account in
# use, not from documentation. Perplexity's `sonar` models are the obvious
# first choice on paper but return HTTP 402 on a free-tier key, so they sit
# last as a best-effort extra. Notably, the *same* model without the suffix
# (google/gemini-2.5-flash) answers from stale training data — it confidently
# quoted a 2023 interest rate — which is exactly the failure mode the ":online"
# suffix exists to prevent, and is worth demonstrating live.
SEARCH_MODELS = [
    "google/gemini-2.5-flash:online",
    "openai/gpt-4o-mini:online",
    "perplexity/sonar",
]

SEARCH_TIMEOUT = 90  # seconds — a cold research call is slow by nature


class SearchError(Exception):
    """Raised when no search backend could be reached."""


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
    """Run the live web search step.

    Returns dict: {findings, citations, model, provider, latency_ms, query}

    `on_stage(stage_label, detail)` is called as the pipeline advances so the
    flip-board in the UI has something real to show. It must never raise.
    """
    query = build_research_query(transaction_type, bank, residency_phrase, state)
    prompt = _search_prompt(transaction_type, bank, residency_phrase, state)

    def stage(label, detail=""):
        if on_stage:
            try:
                on_stage(label, detail)
            except Exception:
                pass

    last_error = None
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
            last_error = exc
            continue

    stage("Search unavailable", "")
    raise SearchError(
        f"Web research unavailable ({type(last_error).__name__}: {last_error})"
    )
