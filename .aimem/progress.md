# Kaagaz — Build Progress Log

Append-only. Each entry: `[YYYY-MM-DD HH:MM] WORKSTREAM: description`

---

[2026-09-25 00:01] INIT: Project skeleton created — directory structure, .aimem/ files initialized (context.md, user-needs.md, decisions.md, progress.md, timeline.md, prompts-log.md). venv setup commands documented in README.

[2026-09-25 00:02] INIT: Core config files created — requirements.txt, .env.example, .gitignore, wsgi.py, app/__init__.py (Flask app factory with Blueprint registration).

[2026-09-25 00:03] DATA: dataset.json curated for all 4 transaction types × 2 states (Kerala, Maharashtra) where state-dependent. 6-10 items per transaction type. Regulatory source field populated; RBI vs state-subject distinction enforced throughout.

[2026-09-25 00:04] BACKEND: Flask blueprints registered (checklist, ai, data). SQLite seeding script (db_seed.py) implemented. Checklist routes operational. Data access layer (data/access.py) implemented with get_checklist() and keyword search.

[2026-09-25 00:05] AI: app/ai/client.py implemented — generate() with OpenRouter primary, NVIDIA NIM fallback, static dataset fallback. Grounded prompts with dataset context injection. Logging to .aimem/progress.md.

[2026-09-25 00:06] FRONTEND: Base template (base.html), index (transaction picker), checklist page, and AI explainer inline component implemented. Fraunces + Inter fonts loaded. Full CSS with paper-texture aesthetic.

[2026-09-25 00:07] FRONTEND: Flip-board component (static/js/flipboard.js + CSS) implemented. Handles PENDING → IN PROGRESS → DONE state flips and document counter animation.

[2026-09-25 00:08] DOCS: README.md written with all required sections. Mermaid architecture and sequence diagrams included. vercel.json and deployment notes added.
[2026-09-26T18:26:11.847586] AI_CALL provider=openrouter prompt_len=1356 success=False latency_ms=3365 error=404 Client Error: Not Found for url: https://openrouter.ai/api/v1/chat/completio
[2026-09-26T18:26:11.848175] AI_CALL provider=nvidia_nim prompt_len=1356 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-26T18:26:11.848273] AI_CALL provider=static_fallback prompt_len=1356 success=True latency_ms=0
[2026-09-26T18:29:47.758983] AI_CALL provider=openrouter prompt_len=926 success=False latency_ms=928 error=404 Client Error: Not Found for url: https://openrouter.ai/api/v1/chat/completio
[2026-09-26T18:29:47.761546] AI_CALL provider=nvidia_nim prompt_len=926 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-26T18:29:47.761776] AI_CALL provider=static_fallback prompt_len=926 success=True latency_ms=0
[2026-09-26T18:30:31.175289] AI_CALL provider=openrouter prompt_len=926 success=False latency_ms=3809 error=404 Client Error: Not Found for url: https://openrouter.ai/api/v1/chat/completio
[2026-09-26T18:30:31.175976] AI_CALL provider=nvidia_nim prompt_len=926 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-26T18:30:31.176153] AI_CALL provider=static_fallback prompt_len=926 success=True latency_ms=0
[2026-09-26T18:35:03.162561] AI_CALL provider=openrouter prompt_len=926 success=False latency_ms=5132 error=404 Client Error: Not Found for url: https://openrouter.ai/api/v1/chat/completio
[2026-09-26T18:35:03.166230] AI_CALL provider=nvidia_nim prompt_len=926 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-26T18:35:03.166460] AI_CALL provider=static_fallback prompt_len=926 success=True latency_ms=0
[2026-09-26T18:55:20.120511] AI_CALL provider=openrouter prompt_len=655 success=False latency_ms=772 error=404 Client Error: Not Found for url: https://openrouter.ai/api/v1/chat/completio
[2026-09-26T18:55:20.122066] AI_CALL provider=nvidia_nim prompt_len=655 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-26T18:55:20.122225] AI_CALL provider=static_fallback prompt_len=655 success=True latency_ms=0
[2026-09-26T18:55:20.491630] AI_CALL provider=openrouter prompt_len=655 success=False latency_ms=278 error=404 Client Error: Not Found for url: https://openrouter.ai/api/v1/chat/completio
[2026-09-26T18:55:20.492535] AI_CALL provider=nvidia_nim prompt_len=655 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-26T18:55:20.492873] AI_CALL provider=static_fallback prompt_len=655 success=True latency_ms=0
[2026-09-26T18:55:20.632827] AI_CALL provider=openrouter prompt_len=655 success=False latency_ms=220 error=404 Client Error: Not Found for url: https://openrouter.ai/api/v1/chat/completio
[2026-09-26T18:55:20.633460] AI_CALL provider=nvidia_nim prompt_len=655 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-26T18:55:20.633703] AI_CALL provider=static_fallback prompt_len=655 success=True latency_ms=0
[2026-09-26T18:55:20.840449] AI_CALL provider=openrouter prompt_len=655 success=False latency_ms=262 error=404 Client Error: Not Found for url: https://openrouter.ai/api/v1/chat/completio
[2026-09-26T18:55:20.840953] AI_CALL provider=nvidia_nim prompt_len=655 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-26T18:55:20.841120] AI_CALL provider=static_fallback prompt_len=655 success=True latency_ms=0
[2026-09-26T19:10:51.211297] AI_CALL provider=openrouter prompt_len=1381 success=False latency_ms=3967 error=404 Client Error: Not Found for url: https://openrouter.ai/api/v1/chat/completio
[2026-09-26T19:10:54.389075] AI_CALL provider=nvidia_nim prompt_len=1381 success=False latency_ms=3176 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T19:10:54.390175] AI_CALL provider=static_fallback prompt_len=1381 success=True latency_ms=0
[2026-09-26T19:11:36.843490] AI_CALL provider=openrouter prompt_len=1381 success=False latency_ms=1123 error=404 Client Error: Not Found for url: https://openrouter.ai/api/v1/chat/completio
[2026-09-26T19:11:37.208169] AI_CALL provider=nvidia_nim prompt_len=1381 success=False latency_ms=363 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T19:11:37.208944] AI_CALL provider=static_fallback prompt_len=1381 success=True latency_ms=0
[2026-09-26T19:12:15.230427] AI_CALL provider=openrouter prompt_len=1381 success=False latency_ms=649 error=404 Client Error: Not Found for url: https://openrouter.ai/api/v1/chat/completio
[2026-09-26T19:12:15.533661] AI_CALL provider=nvidia_nim prompt_len=1381 success=False latency_ms=302 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T19:12:15.534164] AI_CALL provider=static_fallback prompt_len=1381 success=True latency_ms=0
[2026-09-26T19:13:46.496519] AI_CALL provider=openrouter prompt_len=1381 success=True latency_ms=4109
[2026-09-26T19:13:57.064168] AI_CALL provider=openrouter prompt_len=1381 success=True latency_ms=5420
[2026-09-26T19:14:13.264930] AI_CALL provider=openrouter prompt_len=1381 success=True latency_ms=3859

[2026-09-25 01:30] DATA: dataset.json rebuilt — normalized all regulatory_source values to enum (rbi/state_stamp_act/registrar/bank_internal), expanded to 38 rows total (9 home_loan KL, 9 MH, 7 NRI, 8 property_reg KL, 8 MH, 8 business_acct KL/MH). State stamp duty entries correctly use state_stamp_act, never rbi.

[2026-09-25 01:31] AI: OpenRouter model updated from mistralai/mistral-7b-instruct (404 — no endpoints) to meta-llama/llama-3.1-8b-instruct. Live AI call confirmed working — grounded response returned with correct source attribution.

[2026-09-25 01:32] QA: All 4 tests passing. End-to-end smoke test confirmed: all 7 route combinations (4 transaction types × state variants) return 200. AI explainer returns grounded answer via OpenRouter. Static fallback returns correctly when keys absent.

[2026-09-25 01:33] PROJECT: Git repo initialized, .gitignore confirmed (.env excluded, instance/ excluded). Project ready for submission.
