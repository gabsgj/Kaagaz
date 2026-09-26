import os
import time
import json
import requests
from datetime import datetime

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
NVIDIA_NIM_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
OPENROUTER_MODEL = "mistralai/mistral-7b-instruct"
NVIDIA_NIM_MODEL = "meta/llama-3.1-8b-instruct"
TIMEOUT = 8  # seconds

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

def _call_openrouter(system_prompt: str, user_prompt: str, max_tokens: int) -> str:
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
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.2
    }
    resp = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()

def _call_nvidia_nim(system_prompt: str, user_prompt: str, max_tokens: int) -> str:
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
        "temperature": 0.2
    }
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
