"""
Kaagaz — Step 2 of the research pipeline: synthesis.

Takes the raw findings + cited URLs from the search step and turns them into a
strict JSON checklist. The generation step deliberately goes through the same
OpenRouter -> NVIDIA NIM fallback chain the rest of the app uses, so synthesis
degrades independently of search.

Two honesty rules are enforced structurally, not just asked for in the prompt:

1. Nothing may be attributed to the RBI that is really a state matter. A model
   that files stamp duty under `rbi` is corrected to `state_stamp_act` unless
   the item text makes clear it is a genuine RBI rule.
2. A cost the model could not source becomes the explicit string
   "not publicly disclosed — contact the bank directly", never a number.
"""

import re

from ..ai.client import generate_json

# Regulatory buckets. The distinction is load-bearing for this product:
# users routinely assume the RBI sets stamp duty. It does not.
REGULATORY_SOURCES = {
    "rbi": "rbi",
    "state_stamp_act": "state_stamp_act",
    "registrar": "registrar",
    "bank_internal": "bank_internal",
}

REGULATORY_LABELS = {
    "rbi": "RBI rules",
    "state_stamp_act": "State stamp act",
    "registrar": "Registrar / state",
    # No apostrophes in these labels: they are rendered from Python, so Jinja
    # HTML-escapes them to &#39; and any consumer matching on the plain string
    # misses. "Bank policy" is also easier to read in the narrow per-item slot.
    "bank_internal": "Bank policy",
}

NOT_DISCLOSED = "Not publicly disclosed — contact the bank directly"
NO_STATE = "No state-specific rules apply to this step"

SYSTEM_PROMPT = """You turn web-research notes about an Indian banking \
transaction into a strict JSON checklist. You never add facts that are not in \
the notes. Output JSON only, no prose, no markdown fence.

Schema:
{
  "summary": "2-3 sentences a non-expert can act on. What this transaction \
involves, and what is likely to trip the applicant up.",
  "items": [
    {
      "step_order": 1,
      "document_name": "Short noun phrase, title case, max 8 words",
      "plain_explanation": "One or two sentences: what it is and why the bank \
wants it",
      "where_to_obtain": "Specific issuing place, not a generic 'the bank'",
      "approx_cost_min": number or null,
      "approx_cost_max": number or null,
      "approx_time_days": number or null,
      "regulatory_source": "rbi | state_stamp_act | registrar | bank_internal",
      "depends_on": "Exact document_name of an earlier step this needs, or empty \
string",
      "source_note": "Which source established this item"
    }
  ],
  "interest_rate_range": "A BAND with a percentage sign, e.g. \"8.50% - 9.75% \
p.a.\". Never a single number. Empty string if the notes gave no rate.",
  "processing_fee_note": "Fee with amount or basis, or \"Not publicly disclosed \
— contact the bank directly\"",
  "regulatory_note": "One or two sentences separating what the RBI governs from \
what the state stamp act / registrar governs, for THIS transaction. If the \
transaction has no state-level component, say so explicitly.",
  "disclosures": ["Things the notes could not confirm, stated plainly"]
}

Rules:
- GRANULARITY IS THE POINT. The user is standing at a bank counter with a
  printed list. "Income Documents" is useless; "Last 3 months' salary slips"
  and "Latest ITR acknowledgement (2 years)" are useful. Split every bundle
  into its individual documents, each as its own item. A home loan is normally
  10-18 items, not 5. If a bundle genuinely has no separable parts, do not
  invent parts.
- items must be in the order the applicant actually does them, and must start
  from the very first thing they go and collect.
- Every item needs approx_cost_min/max and approx_time_days filled from the
  notes. null is only correct when the notes genuinely say nothing.
- Costs are whole rupees. NEVER invent a number to fill the field.
- interest_rate_range is a BAND such as "8.50% - 9.75% p.a.". If the notes
  give a floating rate and a band, use the band. If they give only a single
  published range like "8.60% onwards", widen it honestly and say so, e.g.
  "8.60% - 11.00% p.a. (bank publishes a floor of 8.60% p.a.)". If truly
  nothing, use the empty string — never guess a band.
- regulatory_source is about WHO imposes the requirement, not how central it is:
  - "rbi" only for genuine RBI rules: KYC, account-opening norms, FEMA \
declarations, loan-processing norms, RBI-directed rate or disclosure rules.
  - "state_stamp_act" only for stamp duty and adhesive stamps under a state \
stamp act.
  - "registrar" for sub-registrar fees, registration charges, mutation, \
encumbrance certificates, ROC/inspectorate fees.
  - "bank_internal" for the bank's own credit policy, internal forms, cheque \
book or locker charges, anything the bank alone decides.
- If the notes are thin, return fewer items. A short accurate checklist beats a \
long speculative one.
"""


def build_user_prompt(transaction_type, bank, residency_phrase, state, findings,
                      citations):
    bank_part = bank or "any major Indian bank"
    state_part = state or "not state-specific"
    if citations:
        lines = "\n".join(
            "- [{i}] {t} — {u}".format(
                i=i + 1,
                t=(c.get("title") or "untitled").strip()[:120],
                u=c.get("url", ""),
            )
            for i, c in enumerate(citations)
        )
        source_block = "SOURCES CONSULTED:\n" + lines
    else:
        source_block = "SOURCES CONSULTED: none were returned by the search step."

    return (
        f"TRANSACTION: {transaction_type}\n"
        f"BANK: {bank_part}\n"
        f"STATE: {state_part}\n"
        f"APPLICANT: {residency_phrase}\n\n"
        "RESEARCH NOTES FROM THE WEB:\n"
        "---------------------------------------\n"
        f"{findings}\n"
        "---------------------------------------\n\n"
        f"{source_block}\n\n"
        "Turn these notes into the JSON checklist. Where the notes mark a figure "
        "as undisclosed, carry that through into the matching field rather than "
        "substituting an estimate."
    )


# ── Structural honesty enforcement ──────────────────────────────────────────

_STATE_MARKERS = (
    "stamp duty", "stamp paper", "adhesive stamp", "non-judicial stamp",
    "registration fee", "registration charge", "registration charges",
    "sub-registrar", "sub registrar", "subregistrar", "mutation fee",
    "encumbrance certificate fee", "khata", "mutation",
)

_RBI_MARKERS = (
    "kyc", "know your customer", "fema", "nre account", "nro account",
    "nri account", "rbi", "repatriation", "vostro", "net banking",
    "core banking", "rbi directive",
)

_BANK_MARKERS = (
    "internal", "bank's own", "bank policy", "cheque book", "locker",
    "bank charges", "processing fee charged by the bank", "credit policy",
    "bank requirement", "the bank may", "bank may",
)


def _coerce_source(item):
    src = (item.get("regulatory_source") or "").strip().lower().replace("-", "_")
    src = src.replace(" ", "_")
    if src in REGULATORY_SOURCES:
        return src
    blob = " ".join(
        str(item.get(k) or "") for k in
        ("document_name", "plain_explanation", "where_to_obtain", "source_note")
    ).lower()

    if any(m in blob for m in _STATE_MARKERS):
        return "state_stamp_act"
    if any(m in blob for m in _BANK_MARKERS):
        return "bank_internal"
    if any(m in blob for m in _RBI_MARKERS):
        return "rbi"
    return "bank_internal"


def _rbi_stamp_duty_violations(answer):
    """Find items the model filed under RBI that are plainly state matters."""
    bad = []
    for item in answer.get("items", []):
        if item.get("regulatory_source") != "rbi":
            continue
        blob = " ".join(
            str(item.get(k) or "") for k in
            ("document_name", "plain_explanation", "where_to_obtain")
        ).lower()
        if any(m in blob for m in _STATE_MARKERS):
            bad.append(item)
    return bad


def _fix_state_misattribution(answer):
    """Re-file RBI-attributed state items. See `_rbi_stamp_duty_violations`.

    This is the single most important correctness rule in the product, so it is
    enforced in code rather than trusted to the prompt.
    """
    for item in _rbi_stamp_duty_violations(answer):
        blob = " ".join(
            str(item.get(k) or "") for k in
            ("document_name", "plain_explanation", "where_to_obtain")
        ).lower()
        if "registrar" in blob or "registration fee" in blob or "mutation" in blob:
            item["regulatory_source"] = "registrar"
        else:
            item["regulatory_source"] = "state_stamp_act"
    return answer


def _coerce_item(raw, index):
    def num(key):
        v = raw.get(key)
        if v is None or v == "":
            return None
        try:
            n = int(round(float(str(v).replace(",", "").replace("₹", "").strip())))
        except (TypeError, ValueError):
            return None
        return max(0, n)

    cost_min = num("approx_cost_min")
    cost_max = num("approx_cost_max")
    if cost_min is not None and cost_max is not None and cost_min > cost_max:
        cost_min, cost_max = cost_max, cost_min
    # A zero cost with a zero max is just "free" — keep it, it is meaningful.
    days = num("approx_time_days")
    if days is not None and days > 365:
        days = 365

    name = (raw.get("document_name") or "").strip()
    if not name:
        return None

    return {
        "step_order": index,
        "document_name": name[:120],
        "plain_explanation": (raw.get("plain_explanation") or "").strip()[:800],
        "where_to_obtain": (raw.get("where_to_obtain") or "").strip()[:300] or NOT_DISCLOSED,
        "approx_cost_min": cost_min,
        "approx_cost_max": cost_max,
        "approx_time_days": days,
        "regulatory_source": _coerce_source(raw),
        "depends_on": (raw.get("depends_on") or "").strip()[:120],
        "source_note": (raw.get("source_note") or "").strip()[:300],
    }


def normalize_answer(raw, citations):
    """Coerce a model response into the shape the UI and DB can trust."""
    if not isinstance(raw, dict):
        return None

    items_in = raw.get("items")
    if not isinstance(items_in, list):
        items_in = []
    items = []
    for raw_item in items_in:
        if not isinstance(raw_item, dict):
            continue
        coerced = _coerce_item(raw_item, len(items) + 1)
        if coerced:
            items.append(coerced)

    if not items:
        return None

    # depends_on must point at a step that actually exists in this list
    known = {i["document_name"].lower() for i in items}
    for item in items:
        dep = item["depends_on"].lower()
        if dep and dep not in known:
            # Try to resolve a loose reference, else drop it rather than show
            # a dangling "Requires: ..." line.
            resolved = next((k for k in known if dep in k or k in dep), None)
            item["depends_on"] = resolved or ""

    answer = {
        "summary": (raw.get("summary") or "").strip()[:1200],
        "items": items,
        "interest_rate_range": (raw.get("interest_rate_range") or "").strip()[:120],
        "processing_fee_note": (raw.get("processing_fee_note") or "").strip()[:300],
        "regulatory_note": (raw.get("regulatory_note") or "").strip()[:800],
        "disclosures": [
            str(d).strip()[:300]
            for d in (raw.get("disclosures") or [])
            if str(d).strip()
        ][:10],
        "sources": [
            {"url": c.get("url", ""), "title": c.get("title", "")}
            for c in citations
        ],
    }
    return _fix_state_misattribution(answer)


def synthesize(transaction_type, bank, residency_phrase, state, findings, citations):
    """Run the generation step over the search findings.

    Returns dict with answer / provider / model, or answer=None if the model
    chain produced nothing usable — the caller then degrades gracefully.
    """
    system_prompt = SYSTEM_PROMPT
    user_prompt = build_user_prompt(
        transaction_type, bank, residency_phrase, state, findings, citations
    )
    result = generate_json(system_prompt, user_prompt, max_tokens=2200,
                           temperature=0.1)
    if result["data"] is None:
        return {"answer": None, "provider": result["source"], "model": "",
                "raw": result["raw"]}
    return {
        "answer": normalize_answer(result["data"], citations),
        "provider": result["source"],
        "model": "",
        "raw": result["raw"],
    }
