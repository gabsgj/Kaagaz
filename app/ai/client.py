import os
import re
import time
import json
import requests
from datetime import datetime

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
NVIDIA_NIM_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

# Provider order is unchanged from Phase 1: OpenRouter first, NVIDIA NIM
# second. What changed in Phase 2 is the *model* on OpenRouter.
#
# gpt-4o-mini is now primary. The research pipeline asks for strict JSON over a
# ~6k-token grounding prompt, and llama-3.1-8b was returning prose and
# truncated JSON often enough to drop whole research runs into the unstructured
# fallback. gpt-4o-mini returns valid JSON essentially every time and costs
# roughly $0.00005 per call, so reliability is effectively free here.
# llama-3.1-8b stays as the second attempt because it is ~6x cheaper still.
OPENROUTER_MODELS = ["openai/gpt-4o-mini", "meta-llama/llama-3.1-8b-instruct"]
NVIDIA_NIM_MODEL = "meta/llama-3.1-8b-instruct"
# Retained for callers that want a single name.
OPENROUTER_MODEL = OPENROUTER_MODELS[0]

# Research generation runs on a long, structured prompt, so it gets a long
# ceiling. Still bounded, so a wedged provider can never hang the request.
TIMEOUT = 60  # seconds

def _build_prompt(term: str, context_rows: list) -> tuple[str, str]:
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

def _call_openrouter_model(model, system_prompt, user_prompt, max_tokens,
                           temperature, json_mode):
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        raise ValueError("No OpenRouter API key")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://kaagaz.app",
        "X-Title": "Kaagaz"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    resp = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


def _call_openrouter(system_prompt, user_prompt, max_tokens,
                     temperature=0.2, json_mode=False):
    """Walk the OpenRouter model tier list; raise if all of them fail."""
    last = None
    for model in OPENROUTER_MODELS:
        try:
            return _call_openrouter_model(model, system_prompt, user_prompt,
                                          max_tokens, temperature, json_mode)
        except Exception as exc:
            last = exc
    raise last if last else ValueError("No OpenRouter model available")


def _call_nvidia_nim(system_prompt: str, user_prompt: str, max_tokens: int,
                     temperature: float = 0.2, json_mode: bool = False) -> str:
    api_key = os.environ.get("NVIDIA_NIM_API_KEY", "")
    if not api_key:
        raise ValueError("No NVIDIA NIM API key")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": NVIDIA_NIM_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    resp = requests.post(NVIDIA_NIM_API_URL, headers=headers, json=payload, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()

def _static_fallback(term: str, context_rows: list) -> str:
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
        return (
            f"{row['document_name']}: {row['plain_explanation']} "
            f"You can obtain it from: {row['where_to_obtain']}. "
            f"Approximate cost: {cost_str}. Time: {time_str}."
        )
    return (
        f"No specific information found for '{term}' in the Kaagaz database. "
        "Please verify with your bank or relevant government office."
    )

def _log(provider: str, prompt_len: int, success: bool, latency_ms: int, error: str = ""):
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

def generate(term: str, context_rows: list, max_tokens: int = 300) -> dict:
    system_prompt, user_prompt = _build_prompt(term, context_rows)
    prompt_len = len(system_prompt) + len(user_prompt)
    
    # Try OpenRouter
    t0 = time.monotonic()
    try:
        text = _call_openrouter(system_prompt, user_prompt, max_tokens)
        _log("openrouter", prompt_len, True, int((time.monotonic() - t0) * 1000))
        return {"explanation": text, "source": "openrouter"}
    except Exception as e:
        _log("openrouter", prompt_len, False, int((time.monotonic() - t0) * 1000), str(e)[:80])
    
    # Try NVIDIA NIM
    t0 = time.monotonic()
    try:
        text = _call_nvidia_nim(system_prompt, user_prompt, max_tokens)
        _log("nvidia_nim", prompt_len, True, int((time.monotonic() - t0) * 1000))
        return {"explanation": text, "source": "nvidia_nim"}
    except Exception as e:
        _log("nvidia_nim", prompt_len, False, int((time.monotonic() - t0) * 1000), str(e)[:80])
    
    # Static fallback — always succeeds
    t0 = time.monotonic()
    text = _static_fallback(term, context_rows)
    _log("static_fallback", prompt_len, True, int((time.monotonic() - t0) * 1000))
    return {"explanation": text, "source": "static_fallback"}


# ═══════════════════════════════════════════════════════════════════
#  Structured generation — used by the research agent (Phase 2)
#
#  Same provider chain as generate(): OpenRouter -> NVIDIA NIM.
#  Difference: the caller supplies its own system/user prompts and wants
#  parsed JSON back, with a lenient repair pass for models that wrap
#  their output in prose or a ```json fence.
# ═══════════════════════════════════════════════════════════════════

def _call_provider(name, system_prompt, user_prompt, max_tokens, temperature, json_mode):
    if name == "openrouter":
        return _call_openrouter(system_prompt, user_prompt, max_tokens,
                                temperature=temperature, json_mode=json_mode)
    return _call_nvidia_nim(system_prompt, user_prompt, max_tokens,
                            temperature=temperature, json_mode=json_mode)


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


def generate_json(system_prompt: str, user_prompt: str, max_tokens: int = 1800,
                  temperature: float = 0.1) -> dict:
    """Generate a JSON object, walking the OpenRouter -> NIM fallback chain.

    Returns {"data": <parsed dict or None>, "raw": <text>, "source": <provider>}.
    `data` is None when every provider failed — callers must handle that.
    """
    prompt_len = len(system_prompt) + len(user_prompt)
    raw = ""
    for provider in ("openrouter", "nvidia_nim"):
        t0 = time.monotonic()
        try:
            raw = _call_provider(provider, system_prompt, user_prompt,
                                 max_tokens, temperature, json_mode=True)
            data = _extract_json(raw)
            if data is not None:
                _log(provider, prompt_len, True,
                     int((time.monotonic() - t0) * 1000))
                return {"data": data, "raw": raw, "source": provider}
            # Provider answered but not as JSON — one salvage attempt at the
            # next provider, which is usually better at strict formats.
            _log(provider, prompt_len, False,
                 int((time.monotonic() - t0) * 1000), "unparseable JSON")
            if provider == "openrouter":
                continue
        except Exception as e:
            _log(provider, prompt_len, False,
                 int((time.monotonic() - t0) * 1000), str(e)[:80])
    return {"data": None, "raw": raw, "source": "none"}
