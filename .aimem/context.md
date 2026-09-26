# Kaagaz — Project Context

**Last updated:** 2026-09-25

## What this is
Kaagaz is a Flask web app that turns "what documents do I need for X banking transaction" into a single ordered, costed checklist. Target users: Indian residents and NRIs navigating routine banking and financial transactions who discover missing documents only at the counter.

## Architecture (current)

```
kaagaz/
  app/
    __init__.py               — Flask app factory
    checklist/                — Blueprint: transaction picker, checklist rendering
    ai/                       — Blueprint: LLM abstraction (OpenRouter → NIM → static fallback)
    data/                     — dataset.json, db_seed.py, data access layer (SQLite)
    static/                   — CSS, JS (incl. flip-board), fonts
    templates/                — Jinja2 templates
  .aimem/                     — persistent cross-agent context
  tests/
  wsgi.py
  requirements.txt
  .env.example
  README.md
```

## Key constraints
- Python + Flask, Jinja2 templates, vanilla JS/CSS — NO frontend build step
- SQLite for document-requirement dataset; no external DB
- AI calls: plain `requests` against OpenRouter (primary) and NVIDIA NIM (fallback)
- Virtual environment only — never install globally
- English UI only for MVP; copy structured for i18n later
- Two states: Kerala and Maharashtra (state-dependent items only)
- Four transaction types: home_loan, nri_account, property_registration, business_account

## Regulatory separation (CRITICAL)
- RBI regulates: KYC norms, banking/loan-processing, NRI account rules
- State governments regulate: stamp duty, registration fees, adhesive-stamp requirements
- These must NEVER be conflated in UI copy, dataset entries, or AI responses
- `regulatory_source` field on each dataset row enforces this distinction

## AI layer
- `app/ai/client.py` — single `generate(prompt, context, max_tokens)` function
- Provider order: OpenRouter → NVIDIA NIM → static dataset fallback
- All calls grounded: relevant dataset rows passed as context in the prompt
- Model choice: see `.aimem/decisions.md`

## Visual design
- Aesthetic: light paper-collage meets clean vector iconography
- Palette: cream `#F6F1E4` bg, deep indigo `#1E3A5F` primary, vermillion `#B3402F` accent, forest green `#3E6B4F` success
- Typography: Fraunces (serif, headings) + Inter (sans, body) via Google Fonts
- Signature element: split-flap/flip-board CSS/JS component for "X of Y documents ready" counter and PENDING/IN PROGRESS/DONE item state
