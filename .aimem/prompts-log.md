# Kaagaz — Prompts Log

Significant prompts received and how they were interpreted.

---

[2026-09-25 00:01] RECEIVED: Full master build prompt (Section 0-17) from user — the KAAGAZ hackathon build document for IBM Bob 2.0 Hackathon (lablab.ai, Sept 25-27 2026).

INTERPRETATION: This is a complete product specification. Build the entire Kaagaz application end-to-end using parallel subagents for: (1) repo skeleton + .aimem/ init, (2) data curation, (3) backend (Flask + SQLite), (4) AI layer (OpenRouter/NIM/fallback), (5) frontend (templates + CSS + flip-board), (6) docs + deployment config.

Key constraints noted:
- No npm/build step — vanilla JS/CSS only
- No live scraping — hand-curated JSON dataset
- Four transaction types, two states (KL, MH)
- RBI vs state regulatory source MUST be separated
- AI calls must be grounded — never free-form financial claims
- Flip-board component is the highest-risk/highest-payoff visual element; build early
- App must never show blank/broken state even if both AI providers fail
- All work must be reconstructable from .aimem/ for submission evidence
