"""
Kaagaz — AI provider layer.

A single ordered registry of chat-completion providers. `generate()` and
`generate_json()` walk it and return the first usable answer, so adding a
provider is a matter of adding one entry to PROVIDERS.

Three properties this file exists to guarantee:

  1. **A provider with no key is skipped entirely, not called and failed.**
     Asking for an unauthenticated request and treating the 401 as a fallback
     is a wasted round trip on every single call.

  2. **A provider that is present but out of credit is demoted for the rest of
     the process.** The OpenRouter key on this project is a free tier with no
     credit, so every call opened with a guaranteed HTTP 402. That is ~200ms of
     dead latency on every generation, forever. Providers that fail on auth or
     quota are now tripped out of the rotation and the chain goes straight to
     the one that can actually answer.

  3. **Groq's model list is discovered, not hardcoded.** Groq rotates its
     catalogue and availability is per-account, so the model list is fetched
     once from /models and filtered to known instruction-following families.
     A hardcoded list would silently 404 the first time Groq retired a slug.

Provider order is OpenRouter -> Groq -> NVIDIA NIM. OpenRouter leads because
gpt-4o-mini is the best model for the structured research prompt; Groq follows
because it is fast with a usable free tier; NIM is last because it works but is
the slowest of the three.
"""

import os
import re
import time
import json
import threading
import requests
from datetime import datetime

# ── Provider definitions ────────────────────────────────────────────────────

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODELS_URL = "https://api.groq.com/openai/v1/models"
NIM_URL = "https://integrate.api.nvidia.com/v1/chat/completions"


class Provider:
    """One chat-completion endpoint family, with an ordered model list."""

    def __init__(self, name, url, models, key_env, *,
                 supports_json=True, headers=None, referer=None):
        self.name = name
        self.url = url
        self.models = list(models)
        self.key_env = key_env
        self.supports_json = supports_json
        self.headers = headers or {}
        self.referer = referer

    def key(self):
        return (os.environ.get(self.key_env) or "").strip()

    def __repr__(self):
        return "<Provider %s models=%d>" % (self.name, len(self.models))


OPENROUTER = Provider(
    "openrouter",
    OPENROUTER_URL,
    # gpt-4o-mini first: the research pipeline asks for strict JSON over a long
    # grounding prompt, and the alternatives return prose and truncated JSON.
    ["openai/gpt-4o-mini", "meta-llama/llama-3.1-8b-instruct"],
    "OPENROUTER_API_KEY",
    headers={"HTTP-Referer": "https://kaagaz.app", "X-Title": "Kaagaz"},
)

GROQ = Provider(
    "groq",
    GROQ_URL,
    # Populated from /models at runtime. This is only the fallback used if the
    # catalogue call fails, so it should be the shortlist most likely to exist
    # rather than an exhaustive list.
    ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "openai/gpt-oss-120b"],
    "GROQ_API_KEY",
)

NIM = Provider(
    "nvidia_nim",
    NIM_URL,
    # Every one verified live against the account in use: a sweep of all 82
    # models NIM advertises found only 13 that actually answer, and the
    # Phase-1 choice (meta/llama-3.1-8b-instruct) now returns 410 Gone.
    # Ordered on measured JSON-mode latency over a real research request.
    [
        "nvidia/nemotron-3-super-120b-a12b",     # 2.7s, valid JSON
        "mistralai/mistral-nemotron",            # 2.1s, valid JSON
        "meta/llama-3.2-11b-vision-instruct",    # 1.8s, valid JSON
    ],
    "NVIDIA_NIM_API_KEY",
)

# Ordered fallback chain. First entry wins.
PROVIDERS = [OPENROUTER, GROQ, NIM]

# Retained for callers that just want a single model name.
OPENROUTER_MODELS = OPENROUTER.models
NVIDIA_NIM_MODELS = NIM.models
GROQ_MODELS = GROQ.models
OPENROUTER_MODEL = OPENROUTER.models[0]
NVIDIA_NIM_MODEL = NIM.models[0]
GROQ_MODEL = GROQ.models[0]

# Research generation runs on a long, structured prompt, so it gets a long
# ceiling. Still bounded, so a wedged provider can never hang the request.
TIMEOUT = 60  # seconds

# Statuses that mean "this provider cannot serve us right now" rather than
# "this particular request failed": no credit, bad key, gone, throttled.
_DEAD_STATUSES = frozenset({401, 402, 403, 404, 410, 429})


# ── Provider health (circuit breaker) ───────────────────────────────────────
#
# A provider that keeps answering 402 is not going to start answering 200 on
# the next call. Remember that for the life of the process and skip it, so the
# chain goes straight to a provider that works.

_tripped = {}          # provider name -> (reason, tripped_at)
_trip_lock = threading.Lock()
# A tripped provider gets a grace period, after which it is retried — a key
# can be topped up mid-session and there is no signal for that other than
# trying again.
TRIP_TTL_SECONDS = 300


def _is_tripped(provider):
    with _trip_lock:
        entry = _tripped.get(provider.name)
        if not entry:
            return False
        reason, at = entry
        if time.time() - at > TRIP_TTL_SECONDS:
            del _tripped[provider.name]
            return False
        return True


def _trip(provider, reason):
    with _trip_lock:
        _tripped[provider.name] = (reason, time.time())


def _reset_trip(provider):
    with _trip_lock:
        _tripped.pop(provider.name, None)


def provider_health():
    """For the health endpoint: which providers can currently serve."""
    out = []
    for p in PROVIDERS:
        out.append({
            "name": p.name,
            "has_key": bool(p.key()),
            "tripped": _is_tripped(p),
            "models": len(p.models),
        })
    return out


# ── Groq model discovery ────────────────────────────────────────────────────
_groq_models_cache = None
_groq_lock = threading.Lock()

# Groq slugs we know follow instructions and honour json_object. Matched as
# substrings against the discovered catalogue.
_GROQ_PREFERRED = (
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-120b",
    "llama-3.1-8b-instant",
    "meta-llama/llama-4-scout",
    "qwen/qwen3-32b",
    "llama-3.1-70b-versatile",
)
_GROQ_ACCEPT = re.compile(
    r"(llama|qwen|mistral|gemma|deepseek|gpt-oss|kimi)", re.I
)
# Never worth spending a call on. `safeguard` and `guard` are moderation
# models that answer with a safety verdict rather than the requested content,
# and accepting one is worse than having no model at all — it looks like a
# successful call and returns nonsense.
_GROQ_REJECT = re.compile(
    r"(whisper|guard|safeguard|embedding|vision|audio|tts|playai|compound|"
    r"pdb|gguf|orpheus|allam)", re.I
)


def _fetch_groq_models(provider=GROQ):
    """Ask Groq what it will serve, once per process.

    Availability is per-account and the catalogue rotates, so a hardcoded list
    is a list that will 404. The shortlist order encodes preference; anything
    else matching the accept pattern is appended so a new model still works.
    """
    global _groq_models_cache
    with _groq_lock:
        if _groq_models_cache is not None:
            return _groq_models_cache

        api_key = provider.key()
        if not api_key:
            _groq_models_cache = list(provider.models)
            return _groq_models_cache

        discovered = []
        try:
            resp = requests.get(
                GROQ_MODELS_URL,
                headers={"Authorization": "Bearer " + api_key,
                         "Content-Type": "application/json"},
                timeout=15,
            )
            if resp.status_code == 200:
                data = resp.json().get("data") or []
                discovered = [d.get("id", "") for d in data if d.get("id")]
        except Exception:
            discovered = []

        if not discovered:
            _groq_models_cache = list(provider.models)
            return _groq_models_cache

        available = set(discovered)
        ordered = [m for m in _GROQ_PREFERRED if m in available]
        rest = sorted(
            m for m in discovered
            if m not in ordered
            and _GROQ_ACCEPT.search(m)
            and not _GROQ_REJECT.search(m)
        )
        # Preferred first, then anything else usable, then the static
        # shortlist. Note this is a concatenation, not `ordered or rest` — the
        # first version returned only the preferred slice whenever it was
        # non-empty, which silently threw away every fallback model.
        merged = ordered + rest
        _groq_models_cache = merged or list(provider.models)
        return _groq_models_cache


def _reset_groq_cache():
    global _groq_models_cache
    with _groq_lock:
        _groq_models_cache = None


# ── HTTP ────────────────────────────────────────────────────────────────────

def _post(provider, model, system_prompt, user_prompt, max_tokens,
          temperature, json_mode):
    api_key = provider.key()
    if not api_key:
        raise ValueError("no key for %s" % provider.name)

    headers = {"Authorization": "Bearer " + api_key,
               "Content-Type": "application/json"}
    headers.update(provider.headers or {})

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    if json_mode and provider.supports_json:
        payload["response_format"] = {"type": "json_object"}

    resp = requests.post(provider.url, headers=headers, json=payload,
                         timeout=TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    return (data["choices"][0]["message"].get("content") or "").strip()


def _status_of(exc):
    """HTTP status behind an exception, or None."""
    response = getattr(exc, "response", None)
    if response is not None:
        return getattr(response, "status_code", None)
    return None


def _models_for(provider):
    if provider is GROQ:
        return _fetch_groq_models(provider)
    return provider.models


def call_provider(provider, system_prompt, user_prompt, max_tokens,
                  temperature=0.2, json_mode=False):
    """Try every model on one provider.

    Trips the provider out of rotation on auth/quota/gone responses. This lives
    here rather than in the transport so the retry decision sits next to the
    policy, and so it is testable without a live socket.
    """
    last = None
    for model in _models_for(provider):
        try:
            text = _post(provider, model, system_prompt, user_prompt,
                         max_tokens, temperature, json_mode)
            if text:
                _reset_trip(provider)
                return text, model
            last = ValueError("empty response from %s/%s" % (provider.name, model))
        except requests.HTTPError as exc:
            status = _status_of(exc)
            if status in _DEAD_STATUSES:
                # No credit, bad key, gone, or rate-limited: a different model
                # on the same provider will not help, so stop here.
                _trip(provider, "HTTP %s" % status)
            raise
        except Exception as exc:  # noqa: BLE001
            last = exc
    raise last if last else ValueError("no model on %s" % provider.name)


def call_chain(system_prompt, user_prompt, max_tokens, temperature=0.2,
               json_mode=False, on_attempt=None):
    """Walk PROVIDERS in order. Returns (text, provider_name, model)."""
    last = None
    for provider in PROVIDERS:
        if not provider.key():
            continue  # no key configured — not a failure, just not available
        if _is_tripped(provider):
            continue
        if on_attempt:
            try:
                on_attempt(provider)
            except Exception:
                pass
        try:
            text, model = call_provider(provider, system_prompt, user_prompt,
                                       max_tokens, temperature, json_mode)
            return text, provider.name, model
        except Exception as exc:  # noqa: BLE001
            last = exc
    if last is not None:
        raise last
    raise ValueError("no AI provider available — set at least one API key")


# ── Prompt building (unchanged from Phase 1) ────────────────────────────────

def _build_prompt(term: str, context_rows: list) -> tuple:
    context_text = ""
    for row in context_rows[:5]:
        cost_min = row.get('approx_cost_min')
        cost_max = row.get('approx_cost_max')
        if cost_min is not None and cost_max is not None and cost_min != cost_max:
            cost_str = f"\u20b9{cost_min}-\u20b9{cost_max}"
        elif cost_min is not None:
            cost_str = f"\u20b9{cost_min}"
        else:
            cost_str = "Varies"
        time_days = row.get('approx_time_days')
        time_str = f"{time_days} days" if time_days is not None else "Varies"
        context_text += f"- {row['document_name']}: {row['plain_explanation']} (Cost: {cost_str}, Time: {time_str}, Obtain from: {row['where_to_obtain']})\n"
    if not context_text:
        context_text = "No specific dataset entry found for this term."

    system_prompt = (
        "You are a helpful assistant for Kaagaz, an Indian banking document assistant. "
        "Answer questions about banking and financial documents using ONLY the provided context. "
        "Do NOT invent document names, costs, rules, or procedures not present in the context. "
        "Keep answers concise (2-4 sentences). If the context does not contain the answer, say so honestly."
    )
    user_prompt = (
        f"Context from the Kaagaz document database:\n{context_text}\n\n"
        f"Question: What is '{term}' and how does a person obtain it for their banking transaction?"
    )
    return system_prompt, user_prompt


# ── JSON extraction ─────────────────────────────────────────────────────────

def _extract_json(text):
    """Pull a JSON object out of a model response, however it wrapped it."""
    if not text:
        return None
    text = text.strip()
    # Strip ```json ... ``` fences
    fence = re.search(r"```(?:json)?\s*(.+?)\s*```", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    try:
        return json.loads(text)
    except ValueError:
        pass
    # First balanced {...} block
    start = text.find("{")
    while start != -1:
        depth = 0
        in_str = False
        esc = False
        for i in range(start, len(text)):
            ch = text[i]
            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
                continue
            if ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start:i + 1])
                    except ValueError:
                        break
        start = text.find("{", start + 1)
    return None


# ── Logging ─────────────────────────────────────────────────────────────────

def _log(provider, prompt_len, success, latency_ms, error=""):
    log_line = (
        f"[{datetime.utcnow().isoformat()}] AI_CALL provider={provider} "
        f"prompt_len={prompt_len} success={success} latency_ms={latency_ms}"
        + (f" error={error}" if error else "")
    )
    try:
        with open(".aimem/progress.md", "a") as f:
            f.write(log_line + "\n")
    except Exception:
        pass  # never fail on logging


# ═══════════════════════════════════════════════════════════════════════════
# Public API
# ═══════════════════════════════════════════════════════════════════════════

def generate(term: str, context_rows: list, max_tokens: int = 300) -> dict:
    """Plain-language explanation, grounded in the static dataset."""
    system_prompt, user_prompt = _build_prompt(term, context_rows)
    prompt_len = len(system_prompt) + len(user_prompt)

    if context_rows:
        row = context_rows[0]
        cost_min = row.get('approx_cost_min')
        cost_max = row.get('approx_cost_max')
        if cost_min is not None and cost_max is not None and cost_min != cost_max:
            cost_str = f"\u20b9{cost_min}\u2013\u20b9{cost_max}"
        elif cost_min is not None:
            cost_str = f"\u20b9{cost_min}"
        else:
            cost_str = "Varies"
        time_days = row.get('approx_time_days')
        time_str = f"{time_days} day(s)" if time_days is not None else "Varies"
        fallback_text = (
            f"{row['document_name']}: {row['plain_explanation']} "
            f"You can obtain it from: {row['where_to_obtain']}. "
            f"Approximate cost: {cost_str}. Time: {time_str}."
        )
    else:
        fallback_text = (
            f"No specific information found for '{term}' in the Kaagaz database. "
            "Please verify with your bank or relevant government office."
        )

    for provider in PROVIDERS:
        if not provider.key() or _is_tripped(provider):
            continue
        t0 = time.monotonic()
        try:
            text, model = call_provider(provider, system_prompt, user_prompt,
                                       max_tokens, 0.2, False)
            _log(provider.name, prompt_len, True,
                 int((time.monotonic() - t0) * 1000))
            return {"explanation": text, "source": provider.name, "model": model}
        except Exception as e:
            _log(provider.name, prompt_len, False,
                 int((time.monotonic() - t0) * 1000), str(e)[:80])

    _log("static_fallback", prompt_len, True, 0)
    return {"explanation": fallback_text, "source": "static_fallback", "model": ""}


def generate_json(system_prompt: str, user_prompt: str, max_tokens: int = 1800,
                  temperature: float = 0.1) -> dict:
    """Generate a JSON object, walking the provider chain.

    Returns {"data": <parsed dict or None>, "raw": <text>, "source": <provider>}.
    `data` is None when no provider could be used — callers must handle that.
    """
    prompt_len = len(system_prompt) + len(user_prompt)
    raw = ""
    last_provider = None

    for provider in PROVIDERS:
        if not provider.key() or _is_tripped(provider):
            continue
        last_provider = provider.name
        t0 = time.monotonic()
        try:
            text, model = call_provider(provider, system_prompt, user_prompt,
                                       max_tokens, temperature, True)
            raw = text
            data = _extract_json(text)
            if data is not None:
                _log(provider.name, prompt_len, True,
                     int((time.monotonic() - t0) * 1000))
                return {"data": data, "raw": text, "source": provider.name,
                        "model": model}
            # Answered, but not as JSON. Try the next provider, which may be
            # better at strict formats; a 120B open-weights model is markedly
            # more reliable here than an 8B one.
            _log(provider.name, prompt_len, False,
                 int((time.monotonic() - t0) * 1000), "unparseable JSON")
        except Exception as e:
            _log(provider.name, prompt_len, False,
                 int((time.monotonic() - t0) * 1000), str(e)[:80])

    return {"data": None, "raw": raw,
            "source": last_provider or "none", "model": ""}
