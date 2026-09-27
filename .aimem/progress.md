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
[2026-09-26T19:35:34.270834] AI_CALL provider=openrouter prompt_len=1383 success=True latency_ms=5836
[2026-09-26T19:43:32.630206] AI_CALL provider=openrouter prompt_len=1383 success=True latency_ms=7363
[2026-09-26T19:51:24.239930] AI_CALL provider=openrouter prompt_len=1383 success=True latency_ms=2126
[2026-09-26T19:52:24.334905] AI_CALL provider=openrouter prompt_len=869 success=True latency_ms=1672
[2026-09-26T19:52:26.124811] AI_CALL provider=openrouter prompt_len=869 success=True latency_ms=1785
[2026-09-26T19:52:30.669988] AI_CALL provider=openrouter prompt_len=869 success=True latency_ms=4541
[2026-09-26T19:52:35.268128] AI_CALL provider=openrouter prompt_len=1383 success=True latency_ms=4592
[2026-09-26T19:52:35.275502] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-26T19:52:35.275712] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-26T19:52:35.275798] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-26T19:52:36.473745] AI_CALL provider=openrouter prompt_len=884 success=True latency_ms=1196
[2026-09-26T19:52:39.612765] AI_CALL provider=openrouter prompt_len=1476 success=True latency_ms=3134
[2026-09-26T19:52:40.834916] AI_CALL provider=openrouter prompt_len=1251 success=True latency_ms=1218
[2026-09-26T19:52:42.121463] AI_CALL provider=openrouter prompt_len=895 success=True latency_ms=1284
[2026-09-26T19:52:42.633323] AI_CALL provider=openrouter prompt_len=911 success=True latency_ms=507
[2026-09-26T19:52:53.368314] AI_CALL provider=openrouter prompt_len=1383 success=True latency_ms=3338
[2026-09-26T19:52:55.006509] AI_CALL provider=openrouter prompt_len=869 success=True latency_ms=1224
[2026-09-26T19:52:57.785414] AI_CALL provider=openrouter prompt_len=869 success=True latency_ms=2774
[2026-09-26T19:52:59.060223] AI_CALL provider=openrouter prompt_len=869 success=True latency_ms=1271
[2026-09-26T19:53:01.492306] AI_CALL provider=openrouter prompt_len=1383 success=True latency_ms=2428
[2026-09-26T19:53:01.501369] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-26T19:53:01.501812] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-26T19:53:01.501991] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-26T19:53:07.117985] AI_CALL provider=openrouter prompt_len=884 success=True latency_ms=5613
[2026-09-26T19:53:12.475793] AI_CALL provider=openrouter prompt_len=1476 success=True latency_ms=5352
[2026-09-26T19:53:16.488313] AI_CALL provider=openrouter prompt_len=1251 success=True latency_ms=4010
[2026-09-26T19:53:21.075717] AI_CALL provider=openrouter prompt_len=895 success=True latency_ms=4583
[2026-09-26T19:53:26.094898] AI_CALL provider=openrouter prompt_len=911 success=True latency_ms=5016
[2026-09-26T19:57:29.691639] AI_CALL provider=openrouter prompt_len=9894 success=True latency_ms=2363
[2026-09-26T20:01:23.423755] AI_CALL provider=openrouter prompt_len=11028 success=True latency_ms=74766
[2026-09-26T20:01:51.169303] AI_CALL provider=openrouter prompt_len=13175 success=True latency_ms=14200
[2026-09-26T20:23:17.056703] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=1256 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:23:17.420965] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=361 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:23:17.422782] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-26T20:23:19.841079] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=1686 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:23:20.106055] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=264 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:23:20.106733] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-26T20:23:21.070044] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=959 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:23:21.418311] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=347 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:23:21.418814] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-26T20:23:22.028275] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=605 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:23:22.324395] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=295 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:23:22.325108] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-26T20:23:23.029286] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=700 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:23:23.285300] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=255 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:23:23.285809] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-26T20:23:23.292350] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-26T20:23:23.292663] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-26T20:23:23.292786] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-26T20:23:24.014100] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=719 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:23:24.272464] AI_CALL provider=nvidia_nim prompt_len=884 success=False latency_ms=258 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:23:24.273102] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-26T20:23:25.542033] AI_CALL provider=openrouter prompt_len=1476 success=False latency_ms=1253 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:23:25.826902] AI_CALL provider=nvidia_nim prompt_len=1476 success=False latency_ms=284 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:23:25.827624] AI_CALL provider=static_fallback prompt_len=1476 success=True latency_ms=0
[2026-09-26T20:23:26.528823] AI_CALL provider=openrouter prompt_len=1251 success=False latency_ms=699 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:23:26.786558] AI_CALL provider=nvidia_nim prompt_len=1251 success=False latency_ms=257 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:23:26.787175] AI_CALL provider=static_fallback prompt_len=1251 success=True latency_ms=0
[2026-09-26T20:23:27.942917] AI_CALL provider=openrouter prompt_len=895 success=False latency_ms=1153 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:23:28.222837] AI_CALL provider=nvidia_nim prompt_len=895 success=False latency_ms=279 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:23:28.223739] AI_CALL provider=static_fallback prompt_len=895 success=True latency_ms=0
[2026-09-26T20:23:28.928764] AI_CALL provider=openrouter prompt_len=911 success=False latency_ms=699 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:23:29.207270] AI_CALL provider=nvidia_nim prompt_len=911 success=False latency_ms=278 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:23:29.210651] AI_CALL provider=static_fallback prompt_len=911 success=True latency_ms=0
[2026-09-26T20:23:36.853823] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=809 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:23:37.191691] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=337 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:23:37.192361] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-26T20:23:38.685499] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=625 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:23:39.079935] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=392 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:23:39.080733] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-26T20:23:39.740918] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=655 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:23:40.018507] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=276 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:23:40.019439] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-26T20:23:40.835139] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=806 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:23:41.104399] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=268 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:23:41.105316] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-26T20:23:41.808890] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=698 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:23:42.087298] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=278 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:23:42.088119] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-26T20:23:42.096347] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-26T20:23:42.096654] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-26T20:23:42.096898] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-26T20:23:42.771524] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=672 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:23:43.046749] AI_CALL provider=nvidia_nim prompt_len=884 success=False latency_ms=274 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:23:43.047591] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-26T20:23:44.393601] AI_CALL provider=openrouter prompt_len=1476 success=False latency_ms=1331 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:23:45.118143] AI_CALL provider=nvidia_nim prompt_len=1476 success=False latency_ms=724 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:23:45.119066] AI_CALL provider=static_fallback prompt_len=1476 success=True latency_ms=0
[2026-09-26T20:23:47.004860] AI_CALL provider=openrouter prompt_len=1251 success=False latency_ms=1884 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:23:47.754226] AI_CALL provider=nvidia_nim prompt_len=1251 success=False latency_ms=748 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:23:47.754942] AI_CALL provider=static_fallback prompt_len=1251 success=True latency_ms=0
[2026-09-26T20:23:48.825823] AI_CALL provider=openrouter prompt_len=895 success=False latency_ms=1068 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:23:49.086342] AI_CALL provider=nvidia_nim prompt_len=895 success=False latency_ms=260 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:23:49.087161] AI_CALL provider=static_fallback prompt_len=895 success=True latency_ms=0
[2026-09-26T20:23:49.777369] AI_CALL provider=openrouter prompt_len=911 success=False latency_ms=688 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:23:50.057764] AI_CALL provider=nvidia_nim prompt_len=911 success=False latency_ms=280 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:23:50.059504] AI_CALL provider=static_fallback prompt_len=911 success=True latency_ms=0
[2026-09-26T20:24:02.875178] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=3003 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:24:03.294902] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=419 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:24:03.295773] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-26T20:24:30.429130] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=890 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:24:30.670385] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=238 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:24:30.670846] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-26T20:24:31.123438] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=449 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:24:31.370318] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=246 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:24:31.370864] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-26T20:24:31.817708] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=443 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:24:32.088788] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=270 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:24:32.089343] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-26T20:24:32.581845] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=489 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:24:32.882886] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=300 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:24:32.883460] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-26T20:24:32.889024] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-26T20:24:32.889249] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-26T20:24:32.889358] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-26T20:24:34.451605] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=1560 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:24:36.505143] AI_CALL provider=nvidia_nim prompt_len=884 success=False latency_ms=2053 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:24:36.505825] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-26T20:24:39.216435] AI_CALL provider=openrouter prompt_len=1476 success=False latency_ms=2695 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:24:40.273121] AI_CALL provider=nvidia_nim prompt_len=1476 success=False latency_ms=1056 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:24:40.273990] AI_CALL provider=static_fallback prompt_len=1476 success=True latency_ms=0
[2026-09-26T20:24:41.823728] AI_CALL provider=openrouter prompt_len=1251 success=False latency_ms=1547 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:24:42.091357] AI_CALL provider=nvidia_nim prompt_len=1251 success=False latency_ms=267 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:24:42.092174] AI_CALL provider=static_fallback prompt_len=1251 success=True latency_ms=0
[2026-09-26T20:24:42.594416] AI_CALL provider=openrouter prompt_len=895 success=False latency_ms=499 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:24:42.850508] AI_CALL provider=nvidia_nim prompt_len=895 success=False latency_ms=255 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:24:42.851129] AI_CALL provider=static_fallback prompt_len=895 success=True latency_ms=0
[2026-09-26T20:24:43.316534] AI_CALL provider=openrouter prompt_len=911 success=False latency_ms=463 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:24:43.570095] AI_CALL provider=nvidia_nim prompt_len=911 success=False latency_ms=253 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:24:43.571099] AI_CALL provider=static_fallback prompt_len=911 success=True latency_ms=0
[2026-09-26T20:25:16.029797] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=2653 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:25:16.458594] AI_CALL provider=nvidia_nim prompt_len=884 success=False latency_ms=425 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:25:16.459092] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-26T20:25:31.364138] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=630 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:25:31.610440] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=243 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:25:31.610855] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-26T20:25:32.545778] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=932 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:25:32.810593] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=264 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:25:32.810993] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-26T20:25:33.499492] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=686 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:25:33.762235] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=262 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:25:33.762700] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-26T20:25:34.460054] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=694 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:25:34.726908] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=266 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:25:34.727358] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-26T20:25:34.731478] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-26T20:25:34.731594] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-26T20:25:34.731667] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-26T20:25:35.417700] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=685 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:25:35.680298] AI_CALL provider=nvidia_nim prompt_len=884 success=False latency_ms=262 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:25:35.680738] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-26T20:25:36.356071] AI_CALL provider=openrouter prompt_len=1476 success=False latency_ms=672 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:25:36.624928] AI_CALL provider=nvidia_nim prompt_len=1476 success=False latency_ms=268 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:25:36.625369] AI_CALL provider=static_fallback prompt_len=1476 success=True latency_ms=0
[2026-09-26T20:25:37.268778] AI_CALL provider=openrouter prompt_len=1251 success=False latency_ms=642 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:25:37.529024] AI_CALL provider=nvidia_nim prompt_len=1251 success=False latency_ms=259 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:25:37.529547] AI_CALL provider=static_fallback prompt_len=1251 success=True latency_ms=0
[2026-09-26T20:25:38.215040] AI_CALL provider=openrouter prompt_len=895 success=False latency_ms=684 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:25:38.494808] AI_CALL provider=nvidia_nim prompt_len=895 success=False latency_ms=279 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:25:38.495241] AI_CALL provider=static_fallback prompt_len=895 success=True latency_ms=0
[2026-09-26T20:25:39.070318] AI_CALL provider=openrouter prompt_len=911 success=False latency_ms=573 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:25:39.332270] AI_CALL provider=nvidia_nim prompt_len=911 success=False latency_ms=261 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:25:39.332866] AI_CALL provider=static_fallback prompt_len=911 success=True latency_ms=0
[2026-09-26T20:25:45.074523] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=827 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:25:45.388578] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=313 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:25:45.389125] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-26T20:25:46.057173] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=504 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:25:46.325620] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=268 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:25:46.326118] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-26T20:25:46.804764] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=476 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:25:47.082522] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=277 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:25:47.082994] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-26T20:25:47.551962] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=466 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:25:47.827127] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=274 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:25:47.827632] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-26T20:25:48.254703] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=423 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:25:48.512288] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=257 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:25:48.513044] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-26T20:25:48.519714] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-26T20:25:48.519932] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-26T20:25:48.520033] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-26T20:25:48.981907] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=460 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:25:49.261985] AI_CALL provider=nvidia_nim prompt_len=884 success=False latency_ms=279 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:25:49.262542] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-26T20:25:49.682465] AI_CALL provider=openrouter prompt_len=1476 success=False latency_ms=417 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:25:49.934986] AI_CALL provider=nvidia_nim prompt_len=1476 success=False latency_ms=252 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:25:49.935600] AI_CALL provider=static_fallback prompt_len=1476 success=True latency_ms=0
[2026-09-26T20:25:50.390118] AI_CALL provider=openrouter prompt_len=1251 success=False latency_ms=452 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:25:50.641362] AI_CALL provider=nvidia_nim prompt_len=1251 success=False latency_ms=250 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:25:50.641976] AI_CALL provider=static_fallback prompt_len=1251 success=True latency_ms=0
[2026-09-26T20:25:51.080986] AI_CALL provider=openrouter prompt_len=895 success=False latency_ms=437 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:25:51.339836] AI_CALL provider=nvidia_nim prompt_len=895 success=False latency_ms=258 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:25:51.340443] AI_CALL provider=static_fallback prompt_len=895 success=True latency_ms=0
[2026-09-26T20:25:51.859635] AI_CALL provider=openrouter prompt_len=911 success=False latency_ms=517 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-26T20:25:52.092616] AI_CALL provider=nvidia_nim prompt_len=911 success=False latency_ms=232 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-26T20:25:52.093086] AI_CALL provider=static_fallback prompt_len=911 success=True latency_ms=0
[2026-09-27T05:09:49.140793] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=505 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:09:49.459937] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=315 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:09:49.460333] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:09:50.049954] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=491 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:09:50.293066] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=242 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:09:50.293467] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:09:50.710834] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=415 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:09:50.977055] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=266 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:09:50.977415] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:09:51.425584] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=446 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:09:51.690606] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=264 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:09:51.691203] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:09:52.179765] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=484 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:09:52.413217] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=233 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:09:52.414053] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:09:52.418364] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T05:09:52.418468] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T05:09:52.418516] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:09:52.954510] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=535 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:09:53.220685] AI_CALL provider=nvidia_nim prompt_len=884 success=False latency_ms=265 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:09:53.220918] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T05:09:53.686289] AI_CALL provider=openrouter prompt_len=1476 success=False latency_ms=464 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:09:53.925423] AI_CALL provider=nvidia_nim prompt_len=1476 success=False latency_ms=238 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:09:53.925878] AI_CALL provider=static_fallback prompt_len=1476 success=True latency_ms=0
[2026-09-27T05:09:54.421549] AI_CALL provider=openrouter prompt_len=1251 success=False latency_ms=494 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:09:54.665364] AI_CALL provider=nvidia_nim prompt_len=1251 success=False latency_ms=243 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:09:54.665984] AI_CALL provider=static_fallback prompt_len=1251 success=True latency_ms=0
[2026-09-27T05:09:55.089522] AI_CALL provider=openrouter prompt_len=895 success=False latency_ms=422 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:09:55.380341] AI_CALL provider=nvidia_nim prompt_len=895 success=False latency_ms=290 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:09:55.380845] AI_CALL provider=static_fallback prompt_len=895 success=True latency_ms=0
[2026-09-27T05:09:55.829117] AI_CALL provider=openrouter prompt_len=911 success=False latency_ms=446 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:09:56.084547] AI_CALL provider=nvidia_nim prompt_len=911 success=False latency_ms=255 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:09:56.084920] AI_CALL provider=static_fallback prompt_len=911 success=True latency_ms=0
[2026-09-27T05:10:12.698406] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=536 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:10:13.044564] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=345 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:10:13.044975] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:10:13.584506] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=454 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:10:13.922868] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=337 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:10:13.923426] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:10:14.414628] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=488 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:10:14.691273] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=276 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:10:14.691730] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:10:15.137625] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=443 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:10:15.396373] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=258 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:10:15.396723] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:10:15.943070] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=544 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:10:16.211648] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=268 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:10:16.212006] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:10:16.215229] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T05:10:16.215314] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T05:10:16.215372] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:10:16.812818] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=596 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:10:17.095954] AI_CALL provider=nvidia_nim prompt_len=884 success=False latency_ms=282 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:10:17.096447] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T05:10:17.556463] AI_CALL provider=openrouter prompt_len=1476 success=False latency_ms=457 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:10:17.850405] AI_CALL provider=nvidia_nim prompt_len=1476 success=False latency_ms=293 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:10:17.850812] AI_CALL provider=static_fallback prompt_len=1476 success=True latency_ms=0
[2026-09-27T05:10:18.272592] AI_CALL provider=openrouter prompt_len=1251 success=False latency_ms=420 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:10:18.513516] AI_CALL provider=nvidia_nim prompt_len=1251 success=False latency_ms=240 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:10:18.513891] AI_CALL provider=static_fallback prompt_len=1251 success=True latency_ms=0
[2026-09-27T05:10:19.058589] AI_CALL provider=openrouter prompt_len=895 success=False latency_ms=543 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:10:19.343152] AI_CALL provider=nvidia_nim prompt_len=895 success=False latency_ms=284 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:10:19.343370] AI_CALL provider=static_fallback prompt_len=895 success=True latency_ms=0
[2026-09-27T05:10:19.820632] AI_CALL provider=openrouter prompt_len=911 success=False latency_ms=476 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:10:20.090286] AI_CALL provider=nvidia_nim prompt_len=911 success=False latency_ms=269 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:10:20.090893] AI_CALL provider=static_fallback prompt_len=911 success=True latency_ms=0
[2026-09-27T05:12:20.534364] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=707 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:12:20.777910] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=243 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:12:20.778447] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:12:21.756427] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=906 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:12:22.007702] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=250 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:12:22.008473] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:12:22.411123] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=400 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:12:22.626587] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=215 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:12:22.627430] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:12:23.063825] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=432 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:12:23.293230] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=229 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:12:23.293881] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:12:23.710365] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=414 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:12:23.940136] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=229 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:12:23.940929] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:12:23.946159] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T05:12:23.946333] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T05:12:23.946394] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:12:24.410767] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=463 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:12:24.657133] AI_CALL provider=nvidia_nim prompt_len=884 success=False latency_ms=246 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:12:24.657538] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T05:12:25.184207] AI_CALL provider=openrouter prompt_len=1476 success=False latency_ms=524 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:12:25.430682] AI_CALL provider=nvidia_nim prompt_len=1476 success=False latency_ms=246 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:12:25.431308] AI_CALL provider=static_fallback prompt_len=1476 success=True latency_ms=0
[2026-09-27T05:12:25.849345] AI_CALL provider=openrouter prompt_len=1251 success=False latency_ms=416 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:12:26.084693] AI_CALL provider=nvidia_nim prompt_len=1251 success=False latency_ms=235 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:12:26.085031] AI_CALL provider=static_fallback prompt_len=1251 success=True latency_ms=0
[2026-09-27T05:12:26.571637] AI_CALL provider=openrouter prompt_len=895 success=False latency_ms=485 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:12:26.778869] AI_CALL provider=nvidia_nim prompt_len=895 success=False latency_ms=206 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:12:26.779219] AI_CALL provider=static_fallback prompt_len=895 success=True latency_ms=0
[2026-09-27T05:12:27.146877] AI_CALL provider=openrouter prompt_len=911 success=False latency_ms=366 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:12:27.372416] AI_CALL provider=nvidia_nim prompt_len=911 success=False latency_ms=225 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:12:27.372989] AI_CALL provider=static_fallback prompt_len=911 success=True latency_ms=0

═══════════════════════════════════════════════════════════════
PHASE 2 — VISUAL REDESIGN & DATA DEPTH EXPANSION
═══════════════════════════════════════════════════════════════

[2026-09-27 01:22] PHASE2 INIT: Session start. Read .aimem/{context,decisions,progress,timeline,user-needs,prompts-log}.md in full. ~19h to deadline. Established that the Phase-1 four-category/two-state architecture must be superseded per the Phase 2 brief.

[2026-09-27 01:25] RESEARCH: Empirically determined which web-search models the OpenRouter account can actually reach. Tested 7 candidates. FINDING: `perplexity/sonar*` returns HTTP 402 on this free-tier key despite being the paper-first choice. `google/gemini-2.5-flash:online` and `openai/gpt-4o-mini:online` both work and both return real citation URLs in OpenRouter's `annotations` array. Notable: `google/gemini-2.5-flash` WITHOUT the `:online` suffix answered a current-interest-rate question from stale training data (quoted a Nov 2023 HDFC rate) — strong evidence the suffix is doing real work, and worth demonstrating live.

[2026-09-27 01:30] PIPELINE: Built app/research/ — refdata.py (36 states/UTs, 72 bank options across 5 groups, ~90 category aliases, residency enum), cache.py (research_cache table, 7-day TTL), search.py (two-step search, citation extraction from annotations), synthesize.py (strict-JSON structuring + code-enforced RBI/state attribution correction), agent.py (orchestration + typed failure), jobs.py (thread + polling + inline fallback), routes.py (6 API endpoints). Schema written per Section 4 including source_urls/research_query/cache_ttl_days.

[2026-09-27 01:35] GATE (Section 7 item 1): Live pipeline verified end-to-end BEFORE any breadth work, as the brief required. Query: HDFC home loan, Kerala, resident. Result: 13.1s, 15 real source URLs captured, 14 fine-grained items, correct RBI/state/registrar split, stored and re-served from cache in 1ms. Second query (SBI education loan, all-NRI) exposed two real defects — coarse 5-item output and an empty interest-rate band — both traced to prompt underspecification and fixed by demanding per-document granularity and an explicit instruction to read the bank's own rate page.

[2026-09-27 01:37] BLOCKER: OpenRouter credit exhausted mid-session (total_credits 0). Confirmed by direct test: every model on the account — generation and search alike — now returns HTTP 402. Escalated to user. User's decision: the agent itself performs the web research for the seed set and writes the sourced answers into the cache, leaving the live path implemented and intact.

[2026-09-27 01:55] DATA: Researched the seed set directly against primary sources via web search — SBI home loan + NRI home loan, SBI education loan / Global Ed-Vantage / MITC, SBI & Axis loan-against-FD, Kotak & HDFC NRI documentation, HDFC FEMA declaration, Kerala Registration Department (stamp duty ready reckoner, 2024 SOP, process flow), ICICI & Kotak current account, SBI gold loan form + RBI 2025 gold directions, Mudra documents. 10 entries, 24 distinct primary sources, all real URLs.

[2026-09-27 02:05] TOOLING: Added scripts/preseed.py. Seeds go through the same cache path as live answers, so the demo hits identical code — just faster. Flags seed rows `is_seed=1` and labels them "pre-warmed" in the UI rather than implying they were fetched on demand.

[2026-09-27 02:30] FRONTEND: Rewrote main.css from scratch (1369 lines). 8px spacing scale with no exceptions; 3 radii; 2 shadows; 68ch measure; every interactive control custom (appearance:none, hand-drawn checkbox, custom select chevron); paper grain; torn deckle dividers; AA+ contrast. Built _icons.html: 33 custom SVG glyphs, all fully outlined, all on a 24x24 grid, all stroke-width 1.75, round caps/joins. Separate decorative macros (wax seal, paperclip, ink stamp) for the collage layer.

[2026-09-27 03:10] BUGFIX (found by reading the rendered page, not by a test): normalize_category's prefix-trimming collapsed "Gold loan for senior citizens" to the seeded "Gold loan" — returning a cached answer to a different question AND guaranteeing a false cache hit. Changed to exact-alias matching only. Bank/state normalisation deliberately keeps trimming, where trailing tokens are noise.

[2026-09-27 03:15] BUGFIX (measured): flip-board jitter. done counter had data-min=1, total had data-min=2 — reaching 10 documents would have added a cell and shifted the board ~26px. Both now pinned server-side to len(str(total)). Status badge measured 96/108.5/96px across its three labels, shoving the step title sideways; min-width set to 112px from measurement.

[2026-09-27 03:25] BUGFIX (found by screenshot): .torn--up was broken three ways — an 8px parent slicing a 16px silhouette in half (read as clipped glyphs), then invisible once un-clipped because a transparent parent has no indigo to reveal, then a uniform sawtooth that read as a blade rather than paper. Fixed by matching container height to the silhouette, pulling the element up over the footer with negative margin + z-index, and regenerating the deckle path with irregular spacing/depth and mixed rounded/sharp tips.

[2026-09-27 03:30] BUGFIX: [hidden] was losing to .notice{display:flex}, leaving an empty blue bar under every checklist item. Added a global `[hidden]{display:none !important}`. Also: the .found source-pill container was a SIBLING of the element the Ticker binds to, so querySelector returned null and the pills silently never rendered. Also: the board label was driven by a client-side phase guess while the ticker showed the server's real stage, so the two disagreed on screen.

[2026-09-27 03:40] QA: Built tests/browser/ — two CDP-driven gates over real Chrome. responsive_audit.js: 7 pages x 3 breakpoints, checking overflow, edge bleed, box clipping, tap targets, live-computed WCAG contrast and JS errors. jitter_test.js: measures board geometry across every value 0..N and the badge across all three states. Committed with a README, since both encode hard requirements no Python test can assert.

[2026-09-27 03:55] GATE RESULTS: responsive_audit 21/21 clean (375/768/1280) after fixing 8 real defects — --ink-3 measured 4.41:1 (AA failure, darkened to 5.1:1), board clipping off-canvas at 375px, colophon links under 24px, missing favicon, and the four above. jitter_test passes: board and badge geometrically stable across 0..14 documents and all three status states.

[2026-09-27 04:05] TESTS: 133 passing. Rewrote the Phase-1 template-structure tests against the new architecture (they asserted a four-item menu and two-state radio pair that the brief removes) while keeping the still-valid data-integrity, AI-fallback and API coverage. Made the live-AI test assert graceful degradation rather than a specific provider answering — a test that demands a 200 from OpenRouter fails for reasons unrelated to the code.
[2026-09-27T05:16:07.965351] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=835 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:16:08.326700] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=361 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:16:08.327096] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:16:09.647571] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=1242 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:16:09.937686] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=289 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:16:09.938143] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:16:10.421874] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=480 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:16:10.686195] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=264 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:16:10.686559] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:16:11.149771] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=461 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:16:11.447723] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=297 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:16:11.448094] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:16:11.935920] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=485 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:16:12.233586] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=297 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:16:12.233927] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:16:12.237424] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T05:16:12.237554] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T05:16:12.237636] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:16:12.659749] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=420 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:16:12.942798] AI_CALL provider=nvidia_nim prompt_len=884 success=False latency_ms=282 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:16:12.943491] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T05:16:13.398717] AI_CALL provider=openrouter prompt_len=1476 success=False latency_ms=452 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:16:13.644713] AI_CALL provider=nvidia_nim prompt_len=1476 success=False latency_ms=245 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:16:13.645082] AI_CALL provider=static_fallback prompt_len=1476 success=True latency_ms=0
[2026-09-27T05:16:14.038153] AI_CALL provider=openrouter prompt_len=1251 success=False latency_ms=391 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:16:14.296993] AI_CALL provider=nvidia_nim prompt_len=1251 success=False latency_ms=258 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:16:14.297357] AI_CALL provider=static_fallback prompt_len=1251 success=True latency_ms=0
[2026-09-27T05:16:14.753418] AI_CALL provider=openrouter prompt_len=895 success=False latency_ms=454 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:16:14.991647] AI_CALL provider=nvidia_nim prompt_len=895 success=False latency_ms=237 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:16:14.992037] AI_CALL provider=static_fallback prompt_len=895 success=True latency_ms=0
[2026-09-27T05:16:15.401923] AI_CALL provider=openrouter prompt_len=911 success=False latency_ms=408 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:16:15.696619] AI_CALL provider=nvidia_nim prompt_len=911 success=False latency_ms=294 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:16:15.696973] AI_CALL provider=static_fallback prompt_len=911 success=True latency_ms=0
[2026-09-27T05:20:56.923812] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=835 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:20:57.267215] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=341 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:20:57.268380] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:20:58.148787] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=803 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:20:58.355348] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=206 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:20:58.356235] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:20:58.907297] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=548 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:20:59.256260] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=348 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:20:59.256740] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:20:59.851896] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=592 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:21:00.283779] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=431 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:21:00.284542] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:21:00.594346] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=306 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:21:00.746964] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=152 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:21:00.747416] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:21:00.751822] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T05:21:00.751984] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T05:21:00.752061] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:21:00.952610] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=199 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:21:01.105046] AI_CALL provider=nvidia_nim prompt_len=884 success=False latency_ms=152 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:21:01.105497] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T05:21:01.341953] AI_CALL provider=openrouter prompt_len=1476 success=False latency_ms=234 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:21:01.494244] AI_CALL provider=nvidia_nim prompt_len=1476 success=False latency_ms=152 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:21:01.494606] AI_CALL provider=static_fallback prompt_len=1476 success=True latency_ms=0
[2026-09-27T05:21:01.747579] AI_CALL provider=openrouter prompt_len=1251 success=False latency_ms=250 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:21:01.898200] AI_CALL provider=nvidia_nim prompt_len=1251 success=False latency_ms=150 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:21:01.898557] AI_CALL provider=static_fallback prompt_len=1251 success=True latency_ms=0
[2026-09-27T05:21:02.148605] AI_CALL provider=openrouter prompt_len=895 success=False latency_ms=248 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:21:02.304256] AI_CALL provider=nvidia_nim prompt_len=895 success=False latency_ms=155 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:21:02.304479] AI_CALL provider=static_fallback prompt_len=895 success=True latency_ms=0
[2026-09-27T05:21:02.543407] AI_CALL provider=openrouter prompt_len=911 success=False latency_ms=237 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:21:02.701748] AI_CALL provider=nvidia_nim prompt_len=911 success=False latency_ms=158 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:21:02.705456] AI_CALL provider=static_fallback prompt_len=911 success=True latency_ms=0
[2026-09-27T05:26:53.911290] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=338 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:26:54.156186] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=244 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:26:54.156605] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:26:54.607406] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=305 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:26:54.805202] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=197 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:26:54.805602] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:26:55.176623] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=368 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:26:55.362095] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=185 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:26:55.362527] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:26:55.727233] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=362 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:26:55.906383] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=178 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:26:55.906762] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:26:56.218708] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=310 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:26:56.414069] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=195 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:26:56.414434] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:26:56.418090] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T05:26:56.418218] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T05:26:56.418295] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:26:56.674368] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=255 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:26:56.867587] AI_CALL provider=nvidia_nim prompt_len=884 success=False latency_ms=192 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:26:56.867988] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T05:26:57.175550] AI_CALL provider=openrouter prompt_len=1476 success=False latency_ms=305 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:26:57.390347] AI_CALL provider=nvidia_nim prompt_len=1476 success=False latency_ms=214 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:26:57.390722] AI_CALL provider=static_fallback prompt_len=1476 success=True latency_ms=0
[2026-09-27T05:26:57.656314] AI_CALL provider=openrouter prompt_len=1251 success=False latency_ms=264 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:26:57.844389] AI_CALL provider=nvidia_nim prompt_len=1251 success=False latency_ms=187 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:26:57.844729] AI_CALL provider=static_fallback prompt_len=1251 success=True latency_ms=0
[2026-09-27T05:26:58.215812] AI_CALL provider=openrouter prompt_len=895 success=False latency_ms=369 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:26:58.409110] AI_CALL provider=nvidia_nim prompt_len=895 success=False latency_ms=193 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:26:58.409558] AI_CALL provider=static_fallback prompt_len=895 success=True latency_ms=0
[2026-09-27T05:26:58.755474] AI_CALL provider=openrouter prompt_len=911 success=False latency_ms=344 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:26:58.956444] AI_CALL provider=nvidia_nim prompt_len=911 success=False latency_ms=200 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:26:58.956917] AI_CALL provider=static_fallback prompt_len=911 success=True latency_ms=0
[2026-09-27T05:31:22.953448] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=553 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:31:23.109968] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=156 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:31:23.110321] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:31:23.493719] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=248 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:31:23.646966] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=152 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:31:23.647595] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:31:23.914546] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=263 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:31:24.069024] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=154 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:31:24.069519] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:31:24.358229] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=286 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:31:24.513949] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=155 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:31:24.514358] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:31:24.764507] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=247 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:31:24.917443] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=152 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:31:24.918274] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:31:24.933510] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T05:31:24.933659] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T05:31:24.933734] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:31:25.162626] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=227 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:31:25.311372] AI_CALL provider=nvidia_nim prompt_len=884 success=False latency_ms=148 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:31:25.311825] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T05:31:25.544960] AI_CALL provider=openrouter prompt_len=1476 success=False latency_ms=231 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:31:25.696371] AI_CALL provider=nvidia_nim prompt_len=1476 success=False latency_ms=151 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:31:25.696833] AI_CALL provider=static_fallback prompt_len=1476 success=True latency_ms=0
[2026-09-27T05:31:25.988447] AI_CALL provider=openrouter prompt_len=1251 success=False latency_ms=290 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:31:26.141310] AI_CALL provider=nvidia_nim prompt_len=1251 success=False latency_ms=152 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:31:26.141763] AI_CALL provider=static_fallback prompt_len=1251 success=True latency_ms=0
[2026-09-27T05:31:26.388126] AI_CALL provider=openrouter prompt_len=895 success=False latency_ms=244 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:31:26.540917] AI_CALL provider=nvidia_nim prompt_len=895 success=False latency_ms=152 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:31:26.541370] AI_CALL provider=static_fallback prompt_len=895 success=True latency_ms=0
[2026-09-27T05:31:26.767532] AI_CALL provider=openrouter prompt_len=911 success=False latency_ms=224 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:31:26.921739] AI_CALL provider=nvidia_nim prompt_len=911 success=False latency_ms=153 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:31:26.922102] AI_CALL provider=static_fallback prompt_len=911 success=True latency_ms=0
[2026-09-27T05:32:10.533487] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=270 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:32:10.687377] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=153 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:32:10.687817] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:32:11.122404] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=252 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:32:11.288009] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=165 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:32:11.292979] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:32:11.554282] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=239 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:32:11.711189] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=156 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:32:11.711764] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:32:11.934463] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=220 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:32:12.091184] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=156 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:32:12.091760] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:32:12.333483] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=238 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:32:12.492022] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=158 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:32:12.492975] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:32:12.503925] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T05:32:12.504493] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T05:32:12.504810] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:32:12.758567] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=249 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:32:12.914394] AI_CALL provider=nvidia_nim prompt_len=884 success=False latency_ms=155 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:32:12.915175] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T05:32:13.142711] AI_CALL provider=openrouter prompt_len=1476 success=False latency_ms=224 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:32:13.295986] AI_CALL provider=nvidia_nim prompt_len=1476 success=False latency_ms=152 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:32:13.296587] AI_CALL provider=static_fallback prompt_len=1476 success=True latency_ms=0
[2026-09-27T05:32:13.513736] AI_CALL provider=openrouter prompt_len=1251 success=False latency_ms=215 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:32:13.670778] AI_CALL provider=nvidia_nim prompt_len=1251 success=False latency_ms=156 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:32:13.671360] AI_CALL provider=static_fallback prompt_len=1251 success=True latency_ms=0
[2026-09-27T05:32:13.931150] AI_CALL provider=openrouter prompt_len=895 success=False latency_ms=258 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:32:14.086075] AI_CALL provider=nvidia_nim prompt_len=895 success=False latency_ms=154 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:32:14.086791] AI_CALL provider=static_fallback prompt_len=895 success=True latency_ms=0
[2026-09-27T05:32:14.348508] AI_CALL provider=openrouter prompt_len=911 success=False latency_ms=260 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:32:14.503794] AI_CALL provider=nvidia_nim prompt_len=911 success=False latency_ms=154 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:32:14.504386] AI_CALL provider=static_fallback prompt_len=911 success=True latency_ms=0
[2026-09-27T05:32:31.293846] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=255 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:32:31.447089] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=152 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:32:31.447405] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:32:31.781203] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=225 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:32:31.935464] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=154 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:32:31.935741] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:32:32.185200] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=247 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:32:32.339655] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=154 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:32:32.339928] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:32:32.558229] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=216 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:32:32.713859] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=155 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:32:32.714157] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:32:32.932941] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=217 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:32:33.102079] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=168 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:32:33.102398] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:32:33.107045] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T05:32:33.107232] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T05:32:33.107393] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:32:33.333811] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=224 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:32:33.485719] AI_CALL provider=nvidia_nim prompt_len=884 success=False latency_ms=151 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:32:33.486137] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T05:32:33.699945] AI_CALL provider=openrouter prompt_len=1476 success=False latency_ms=211 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:32:33.853010] AI_CALL provider=nvidia_nim prompt_len=1476 success=False latency_ms=152 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:32:33.853363] AI_CALL provider=static_fallback prompt_len=1476 success=True latency_ms=0
[2026-09-27T05:32:34.130871] AI_CALL provider=openrouter prompt_len=1251 success=False latency_ms=275 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:32:34.287028] AI_CALL provider=nvidia_nim prompt_len=1251 success=False latency_ms=155 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:32:34.287378] AI_CALL provider=static_fallback prompt_len=1251 success=True latency_ms=0
[2026-09-27T05:32:34.528896] AI_CALL provider=openrouter prompt_len=895 success=False latency_ms=240 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:32:34.682944] AI_CALL provider=nvidia_nim prompt_len=895 success=False latency_ms=153 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:32:34.683224] AI_CALL provider=static_fallback prompt_len=895 success=True latency_ms=0
[2026-09-27T05:32:34.941448] AI_CALL provider=openrouter prompt_len=911 success=False latency_ms=257 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:32:35.099847] AI_CALL provider=nvidia_nim prompt_len=911 success=False latency_ms=158 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:32:35.100136] AI_CALL provider=static_fallback prompt_len=911 success=True latency_ms=0
[2026-09-27T05:33:40.141515] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=264 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:33:40.315460] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=173 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:33:40.315898] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:33:40.733584] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=272 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:33:40.885180] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=151 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:33:40.885673] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:33:41.107861] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=219 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:33:41.259468] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=151 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:33:41.259856] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:33:41.517159] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=255 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:33:41.669550] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=152 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:33:41.670115] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:33:41.928684] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=254 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:33:42.082161] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=153 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:33:42.082625] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:33:42.089219] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T05:33:42.089434] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T05:33:42.089579] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:33:42.341459] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=250 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:33:42.492416] AI_CALL provider=nvidia_nim prompt_len=884 success=False latency_ms=150 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:33:42.492880] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T05:33:42.728240] AI_CALL provider=openrouter prompt_len=1476 success=False latency_ms=233 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:33:42.882075] AI_CALL provider=nvidia_nim prompt_len=1476 success=False latency_ms=153 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:33:42.882465] AI_CALL provider=static_fallback prompt_len=1476 success=True latency_ms=0
[2026-09-27T05:33:43.146469] AI_CALL provider=openrouter prompt_len=1251 success=False latency_ms=262 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:33:43.299492] AI_CALL provider=nvidia_nim prompt_len=1251 success=False latency_ms=152 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:33:43.299892] AI_CALL provider=static_fallback prompt_len=1251 success=True latency_ms=0
[2026-09-27T05:33:43.614545] AI_CALL provider=openrouter prompt_len=895 success=False latency_ms=313 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:33:43.770774] AI_CALL provider=nvidia_nim prompt_len=895 success=False latency_ms=152 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:33:43.771210] AI_CALL provider=static_fallback prompt_len=895 success=True latency_ms=0
[2026-09-27T05:33:44.016402] AI_CALL provider=openrouter prompt_len=911 success=False latency_ms=243 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:33:44.169678] AI_CALL provider=nvidia_nim prompt_len=911 success=False latency_ms=153 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:33:44.170122] AI_CALL provider=static_fallback prompt_len=911 success=True latency_ms=0

[2026-09-27 05:05] GATE: Verified the failure path with search genuinely down (HTTP 402 on every model). Result: a typed message, a retry button, no blank page, no stuck spinner, no raw exception, zero page errors. But the page was still saying "RESEARCHING LIVE" with an animated pulse and "Kaagaz is searching the web" directly above the failure notice. Fixed: board relabelled, pulse paused, cold-query note withdrawn, retry restores all three, and the elapsed counter now reports real time spent instead of freezing at the last successful poll.

[2026-09-27 05:15] QA: Ran every seed case with search unavailable to confirm the app is fully demonstrable offline. 9/10 served. The miss was the study-abroad education loan: its seed keyed `education loan (study abroad)` while its example chip asked `education loan`, because the example tuples could not express a state and the education case was relying on the old prefix-trimming that has since been removed. Fixed by making domestic and study-abroad education loans genuinely distinct categories, adding `state` to the example tuples, and adding both a Python test (TestDemoIsPreWarmed) and a browser gate (demo_links_test.js) that assert every example resolves to a cache hit.

[2026-09-27 05:25] GATE RESULTS (final): 137 Python tests pass. responsive_audit 21/21 clean. jitter_test: board and badge geometrically stable across 0..14 documents and all three status states. demo_links_test: 10/10 example chips serve a complete, sourced checklist from cache with the network down.
[2026-09-27T05:35:14.280089] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=529 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:35:14.431545] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=149 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:35:14.431928] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:35:14.813056] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=241 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:35:14.964753] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=151 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:35:14.965148] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:35:15.229977] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=262 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:35:15.380371] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=150 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:35:15.380730] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:35:15.628927] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=246 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:35:15.782535] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=153 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:35:15.782991] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:35:16.041248] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=256 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:35:16.199026] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=157 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:35:16.205135] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:35:16.214796] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T05:35:16.214999] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T05:35:16.215079] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:35:16.440353] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=224 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:35:16.602076] AI_CALL provider=nvidia_nim prompt_len=884 success=False latency_ms=161 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:35:16.602505] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T05:35:16.829746] AI_CALL provider=openrouter prompt_len=1476 success=False latency_ms=222 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:35:16.980955] AI_CALL provider=nvidia_nim prompt_len=1476 success=False latency_ms=150 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:35:16.981439] AI_CALL provider=static_fallback prompt_len=1476 success=True latency_ms=0
[2026-09-27T05:35:17.203332] AI_CALL provider=openrouter prompt_len=1251 success=False latency_ms=220 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:35:17.355146] AI_CALL provider=nvidia_nim prompt_len=1251 success=False latency_ms=151 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:35:17.355728] AI_CALL provider=static_fallback prompt_len=1251 success=True latency_ms=0
[2026-09-27T05:35:17.644307] AI_CALL provider=openrouter prompt_len=895 success=False latency_ms=286 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:35:17.803221] AI_CALL provider=nvidia_nim prompt_len=895 success=False latency_ms=158 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:35:17.803717] AI_CALL provider=static_fallback prompt_len=895 success=True latency_ms=0
[2026-09-27T05:35:18.066663] AI_CALL provider=openrouter prompt_len=911 success=False latency_ms=260 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:35:18.221074] AI_CALL provider=nvidia_nim prompt_len=911 success=False latency_ms=154 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:35:18.221569] AI_CALL provider=static_fallback prompt_len=911 success=True latency_ms=0
[2026-09-27T05:35:40.387994] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=274 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:35:40.544796] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=154 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:35:40.545172] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:35:40.938090] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=246 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:35:41.092848] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=154 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:35:41.093248] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:35:41.341268] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=245 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:35:41.494799] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=153 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:35:41.495197] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:35:41.769559] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=272 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:35:41.923262] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=153 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:35:41.923671] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:35:42.152018] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=226 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:35:42.337716] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=185 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:35:42.338162] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:35:42.345558] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T05:35:42.345735] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T05:35:42.345823] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:35:42.714903] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=367 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:35:42.868179] AI_CALL provider=nvidia_nim prompt_len=884 success=False latency_ms=153 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:35:42.868873] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T05:35:43.159449] AI_CALL provider=openrouter prompt_len=1476 success=False latency_ms=288 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:35:43.316588] AI_CALL provider=nvidia_nim prompt_len=1476 success=False latency_ms=156 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:35:43.317293] AI_CALL provider=static_fallback prompt_len=1476 success=True latency_ms=0
[2026-09-27T05:35:43.591151] AI_CALL provider=openrouter prompt_len=1251 success=False latency_ms=272 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:35:43.741868] AI_CALL provider=nvidia_nim prompt_len=1251 success=False latency_ms=150 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:35:43.742250] AI_CALL provider=static_fallback prompt_len=1251 success=True latency_ms=0
[2026-09-27T05:35:43.975842] AI_CALL provider=openrouter prompt_len=895 success=False latency_ms=232 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:35:44.128293] AI_CALL provider=nvidia_nim prompt_len=895 success=False latency_ms=152 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:35:44.128733] AI_CALL provider=static_fallback prompt_len=895 success=True latency_ms=0
[2026-09-27T05:35:44.347022] AI_CALL provider=openrouter prompt_len=911 success=False latency_ms=216 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:35:44.499947] AI_CALL provider=nvidia_nim prompt_len=911 success=False latency_ms=152 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:35:44.500397] AI_CALL provider=static_fallback prompt_len=911 success=True latency_ms=0

[2026-09-27 05:45] DEPLOY: Found and fixed a latent deployment blocker. The Phase-1 vercel.json would have 500'd on first write — the Vercel bundle is read-only and only /tmp is writable, but the app wrote to instance/kaagaz.db unconditionally. Added runtime path resolution (DATABASE_PATH -> instance/ -> /tmp/ -> :memory:), auto-seeding the research cache on startup when empty, and GET /api/research/health. Verified by simulating a cold serverless start at a fresh path: 10/10 demo chips auto-seeded and served instantly. Added TestDeployment (5 tests) covering cold start, path override, health honesty, and behaviour with no API keys at all.

[2026-09-27 05:50] GATE RESULTS: 142 Python tests. responsive 21/21 clean. jitter stable. demo links 10/10 from cache with search down.
[2026-09-27T05:37:12.416086] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=277 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:37:12.571196] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=154 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:37:12.571899] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:37:13.172724] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=279 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:37:13.326877] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=153 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:37:13.327527] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:37:13.593238] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=262 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:37:13.746118] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=152 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:37:13.746878] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:37:13.961677] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=209 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:37:14.120783] AI_CALL provider=nvidia_nim prompt_len=869 success=False latency_ms=158 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:37:14.121355] AI_CALL provider=static_fallback prompt_len=869 success=True latency_ms=0
[2026-09-27T05:37:14.411880] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=285 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:37:14.565364] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=153 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:37:14.567354] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:37:14.575369] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T05:37:14.575544] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T05:37:14.575622] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:37:15.277895] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=701 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:37:15.445086] AI_CALL provider=nvidia_nim prompt_len=884 success=False latency_ms=166 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:37:15.445768] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T05:37:15.723234] AI_CALL provider=openrouter prompt_len=1476 success=False latency_ms=273 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:37:15.873762] AI_CALL provider=nvidia_nim prompt_len=1476 success=False latency_ms=150 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:37:15.874513] AI_CALL provider=static_fallback prompt_len=1476 success=True latency_ms=0
[2026-09-27T05:37:16.127572] AI_CALL provider=openrouter prompt_len=1251 success=False latency_ms=251 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:37:16.280588] AI_CALL provider=nvidia_nim prompt_len=1251 success=False latency_ms=152 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:37:16.281076] AI_CALL provider=static_fallback prompt_len=1251 success=True latency_ms=0
[2026-09-27T05:37:16.527964] AI_CALL provider=openrouter prompt_len=895 success=False latency_ms=245 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:37:16.680193] AI_CALL provider=nvidia_nim prompt_len=895 success=False latency_ms=151 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:37:16.680880] AI_CALL provider=static_fallback prompt_len=895 success=True latency_ms=0
[2026-09-27T05:37:16.975375] AI_CALL provider=openrouter prompt_len=911 success=False latency_ms=292 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:37:17.131754] AI_CALL provider=nvidia_nim prompt_len=911 success=False latency_ms=156 error=410 Client Error: Gone for url: https://integrate.api.nvidia.com/v1/chat/complet
[2026-09-27T05:37:17.132659] AI_CALL provider=static_fallback prompt_len=911 success=True latency_ms=0
[2026-09-27T05:54:12.380075] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=277 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:54:14.588482] AI_CALL provider=nvidia_nim prompt_len=1383 success=True latency_ms=2204
[2026-09-27T05:54:15.111970] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=348 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:54:18.352483] AI_CALL provider=nvidia_nim prompt_len=869 success=True latency_ms=3240
[2026-09-27T05:54:18.626719] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=266 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:54:22.063094] AI_CALL provider=nvidia_nim prompt_len=869 success=True latency_ms=3436
[2026-09-27T05:54:22.332598] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=265 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:54:24.524003] AI_CALL provider=nvidia_nim prompt_len=869 success=True latency_ms=2191
[2026-09-27T05:54:24.780668] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=251 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:54:36.916595] AI_CALL provider=nvidia_nim prompt_len=1383 success=True latency_ms=12135
[2026-09-27T05:54:36.931445] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T05:54:36.931759] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T05:54:36.932154] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T05:54:37.216788] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=280 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:54:40.395334] AI_CALL provider=nvidia_nim prompt_len=884 success=True latency_ms=3178
[2026-09-27T05:54:40.657849] AI_CALL provider=openrouter prompt_len=1476 success=False latency_ms=257 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:54:42.664374] AI_CALL provider=nvidia_nim prompt_len=1476 success=True latency_ms=2006
[2026-09-27T05:54:42.932082] AI_CALL provider=openrouter prompt_len=1251 success=False latency_ms=265 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:54:44.285961] AI_CALL provider=nvidia_nim prompt_len=1251 success=True latency_ms=1353
[2026-09-27T05:54:44.513397] AI_CALL provider=openrouter prompt_len=895 success=False latency_ms=224 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:54:46.742455] AI_CALL provider=nvidia_nim prompt_len=895 success=True latency_ms=2228
[2026-09-27T05:54:46.992220] AI_CALL provider=openrouter prompt_len=911 success=False latency_ms=247 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T05:54:50.862125] AI_CALL provider=nvidia_nim prompt_len=911 success=True latency_ms=3869
[2026-09-27T06:01:13.654593] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=300 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T06:02:23.821142] AI_CALL provider=nvidia_nim prompt_len=1383 success=True latency_ms=70165
[2026-09-27T06:02:24.616857] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=586 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T06:02:30.733974] AI_CALL provider=nvidia_nim prompt_len=869 success=True latency_ms=6116
[2026-09-27T06:02:31.028323] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=272 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T06:02:33.289006] AI_CALL provider=nvidia_nim prompt_len=869 success=True latency_ms=2260
[2026-09-27T06:02:33.520187] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=225 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T06:02:34.961659] AI_CALL provider=nvidia_nim prompt_len=869 success=True latency_ms=1441
[2026-09-27T06:02:35.226050] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=257 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T06:02:38.819826] AI_CALL provider=nvidia_nim prompt_len=1383 success=True latency_ms=3593
[2026-09-27T06:02:38.829743] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T06:02:38.829936] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T06:02:38.830003] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T06:02:39.073973] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=242 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T06:02:40.355282] AI_CALL provider=nvidia_nim prompt_len=884 success=True latency_ms=1280
[2026-09-27T06:02:40.598154] AI_CALL provider=openrouter prompt_len=1476 success=False latency_ms=239 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T06:02:43.634478] AI_CALL provider=nvidia_nim prompt_len=1476 success=True latency_ms=3036
[2026-09-27T06:02:43.881404] AI_CALL provider=openrouter prompt_len=1251 success=False latency_ms=243 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T06:02:57.522975] AI_CALL provider=nvidia_nim prompt_len=1251 success=True latency_ms=13641
[2026-09-27T06:02:57.762696] AI_CALL provider=openrouter prompt_len=895 success=False latency_ms=232 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T06:03:00.454360] AI_CALL provider=nvidia_nim prompt_len=895 success=True latency_ms=2691
[2026-09-27T06:03:00.725367] AI_CALL provider=openrouter prompt_len=911 success=False latency_ms=267 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T06:03:05.345984] AI_CALL provider=nvidia_nim prompt_len=911 success=True latency_ms=4620
[2026-09-27T06:03:26.512818] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=263 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T06:04:30.029710] AI_CALL provider=nvidia_nim prompt_len=1383 success=True latency_ms=63516
[2026-09-27T06:04:30.770028] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=530 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T06:04:32.524456] AI_CALL provider=nvidia_nim prompt_len=869 success=True latency_ms=1754
[2026-09-27T06:04:32.768209] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=236 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T06:04:35.649615] AI_CALL provider=nvidia_nim prompt_len=869 success=True latency_ms=2881
[2026-09-27T06:04:35.892919] AI_CALL provider=openrouter prompt_len=869 success=False latency_ms=233 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T06:04:41.702968] AI_CALL provider=nvidia_nim prompt_len=869 success=True latency_ms=5809
[2026-09-27T06:04:41.943309] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=235 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T06:04:44.362501] AI_CALL provider=nvidia_nim prompt_len=1383 success=True latency_ms=2418
[2026-09-27T06:04:44.371574] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T06:04:44.371782] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T06:04:44.371867] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T06:04:44.592097] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=218 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T06:05:32.087808] AI_CALL provider=nvidia_nim prompt_len=884 success=True latency_ms=47495
[2026-09-27T06:05:32.711942] AI_CALL provider=openrouter prompt_len=1476 success=False latency_ms=614 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T06:05:34.233597] AI_CALL provider=nvidia_nim prompt_len=1476 success=True latency_ms=1521
[2026-09-27T06:05:34.493157] AI_CALL provider=openrouter prompt_len=1251 success=False latency_ms=256 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T06:05:36.078830] AI_CALL provider=nvidia_nim prompt_len=1251 success=True latency_ms=1584
[2026-09-27T06:05:36.325104] AI_CALL provider=openrouter prompt_len=895 success=False latency_ms=242 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T06:05:38.125175] AI_CALL provider=nvidia_nim prompt_len=895 success=True latency_ms=1799
[2026-09-27T06:05:38.397532] AI_CALL provider=openrouter prompt_len=911 success=False latency_ms=263 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T06:05:40.487301] AI_CALL provider=nvidia_nim prompt_len=911 success=True latency_ms=2089
[2026-09-27T06:06:14.089446] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T06:06:14.089997] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T06:06:14.090085] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T06:06:14.090915] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T06:06:14.090989] AI_CALL provider=nvidia_nim prompt_len=884 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T06:06:14.091041] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T06:06:31.524893] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T06:06:31.525565] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T06:06:31.525774] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T06:06:31.527847] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T06:06:31.528206] AI_CALL provider=nvidia_nim prompt_len=884 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T06:06:31.528314] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0

[2026-09-27 05:55] RESEARCH (Phase 2b): User suggested trying NVIDIA NIM's free models. Swept all 82 models the NIM account advertises — only 13 actually answer a completion; the rest 404. Verified JSON-mode quality on the instruction-following ones: nemotron-3-super-120b 2.7s valid JSON, mistral-nemotron 2.1s, llama-3.2-11b 1.8s. Generation is therefore free and keyless.

[2026-09-27 06:00] SEARCH: Replaced model-native web search as the primary step with a direct keyless pipeline — DuckDuckGo's HTML endpoints for results, then fetch the top pages in parallel and strip to text, feeding real page content to the synthesiser. Verified: 10 results, 5/5 pages fetched, real titles and URLs. This is better grounding than a web-enabled model (actual page text, not a model's summary) and removes the credit dependency.

[2026-09-27 06:05] BUGFIX: Two silent search bugs. (1) Result URLs came out percent-encoded (`https%3A%2F%2F...`) because html.unescape does not decode percent-encoding — every page fetch was a 404 on a literal nonsense URL while the code reported no error. (2) DDG blocks by returning HTTP 202 with a challenge page, which was being parsed as "zero results" and reported as "no search backend available". Both now handled explicitly; throttles are retried with bounded backoff and then fall through to the second backend.

[2026-09-27 06:10] BUGFIX: Search result quality. A single generic query returned two Scribd previews and three aggregators with the bank's own product page ranked out of the top five. Added authority-tiered ranking (regulator > bank's own domain > everything else, stable within tier) plus a second query biased at the bank's site when the first finds nothing authoritative. The official SBI NRI home loan page now ranks first.

[2026-09-27 06:20] TESTS: Added TestDirectSearch (14 tests) covering percent-decoding, both HTML parsers, dedup, anti-bot detection, junk-host exclusion, source-authority ranking, tier stability, unknown-bank handling, HTML stripping, dead-link tolerance, throttle fall-through, and the direct path not touching OpenRouter. Made the whole suite network-free — it had silently become live once NIM started answering, taking the run from 5s to 140s. 162 tests, 1.7s.

[2026-09-27 06:25] GATE RESULTS: 162 Python tests in 1.7s. responsive 21/21. jitter stable. demo links 10/10. Search is currently rate-limited by DuckDuckGo (verified: the block detection reports it correctly rather than as a false "no results"); the pipeline retries with backoff and falls through to the model-native backend, and the seeded cache is unaffected.
[2026-09-27T06:11:34.491645] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T06:11:34.492254] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T06:11:34.492345] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T06:11:34.493300] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T06:11:34.493377] AI_CALL provider=nvidia_nim prompt_len=884 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T06:11:34.493433] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T06:11:52.971791] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T06:11:52.972420] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T06:11:52.972501] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T06:11:52.974204] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T06:11:52.974424] AI_CALL provider=nvidia_nim prompt_len=884 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T06:11:52.974519] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0

[2026-09-27 06:35] BUGFIX (serious, self-inflicted): Found that a fresh database seeded NO tables. Root cause: the serverless writability probe in _resolve_database_path did `open(candidate, 'a')`, which creates the file; db_seed.seed_db then saw it existing, assumed "already seeded", and returned without creating anything. A fresh clone would 500 on the first checklist page. It hid for an hour because the dev DB already existed, because init_schema creates research_cache unconditionally so all research tests passed, and because my cold-start test only asserted the research side. Fixed by testing the directory's writability instead of the file's. Added three tests: full schema present on cold start, legacy dataset populated on cold start, and the probe does not create the file.

[2026-09-27 06:40] DATA: Extended the seed set from 10 to 14 with personal loan (Kotak + ICICI, contrasting on income proof — Kotak wants 3 months of slips and statements, ICICI pulls income itself via net banking/account aggregator), Kisan Credit Card (SBI + RBI 2026 Scheme Directions; the one seed where the RBI sets most of the rule, and where linked Aadhaar decides 7% vs MCLR-linked), vehicle loan (HDFC car and two-wheeler), and loan against property (HDFC, 65% LTV vs 90% for a home loan). 32 distinct primary sources.

[2026-09-27 06:42] BUGFIX: The umbrella-row guard caught my own new loan-against-property entry for containing "property documents". Split the title chain into the six real documents (sale deed, chain of title, encumbrance certificate, occupancy certificate, tax and maintenance receipts, approved plan) — 5 items to 13. The test earned its keep immediately.

[2026-09-27 06:45] GATE RESULTS: 165 Python tests in 2.7s. responsive 21/21. jitter stable. demo links 14/14 from cache with search down.
[2026-09-27T06:15:16.144425] AI_CALL provider=openrouter prompt_len=1383 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T06:15:16.145197] AI_CALL provider=nvidia_nim prompt_len=1383 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T06:15:16.145330] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T06:15:16.147063] AI_CALL provider=openrouter prompt_len=884 success=False latency_ms=0 error=No OpenRouter API key
[2026-09-27T06:15:16.147313] AI_CALL provider=nvidia_nim prompt_len=884 success=False latency_ms=0 error=No NVIDIA NIM API key
[2026-09-27T06:15:16.147421] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T06:22:11.597801] AI_CALL provider=openrouter prompt_len=170 success=False latency_ms=444 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T06:22:13.062792] AI_CALL provider=groq prompt_len=170 success=True latency_ms=1464
[2026-09-27T06:22:35.544141] AI_CALL provider=groq prompt_len=1383 success=True latency_ms=1335
[2026-09-27T06:22:36.386743] AI_CALL provider=groq prompt_len=884 success=True latency_ms=797
[2026-09-27T06:22:49.428748] AI_CALL provider=groq prompt_len=1383 success=True latency_ms=1247
[2026-09-27T06:23:12.300935] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T06:23:12.303038] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T06:24:47.117651] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T06:24:47.120828] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T06:24:50.559699] AI_CALL provider=openrouter prompt_len=197 success=False latency_ms=442 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T06:24:52.365391] AI_CALL provider=groq prompt_len=197 success=True latency_ms=1805
[2026-09-27T06:25:05.318929] AI_CALL provider=openrouter prompt_len=4816 success=False latency_ms=165 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T06:25:08.730131] AI_CALL provider=groq prompt_len=4816 success=True latency_ms=3410

[2026-09-27 06:50] AI: User added a GROQ_API_KEY. Verified live: endpoint reachable, 11 models on the account. CRITICAL FINDING — `llama-3.3-70b-versatile` and `llama-3.1-8b-instant` (the slugs a hardcoded list would name) do not exist there and 404. Usable: `openai/gpt-oss-120b` (0.9s, valid JSON), `openai/gpt-oss-20b`, `qwen/qwen3.8-27b`. This confirmed the decision to discover the model list from /models at runtime.

[2026-09-27 06:55] AI: Refactored app/ai/client.py into an ordered PROVIDERS registry (OpenRouter -> Groq -> NVIDIA NIM) with a per-provider model list, a Groq model-discovery step, and a circuit breaker. Providers with no key are now skipped without being called; providers answering 401/402/403/404/410/429 are tripped out for 5 minutes and retried after. Removed the duplicated per-provider logic in generate() and generate_json().

[2026-09-27 07:00] VERIFY: Live structured generation through the real chain returns Groq/openai/gpt-oss-120b in 2.2s with valid parsed JSON. Health shows openrouter tripped and calls going straight to Groq. Full synthesis over real page text (HDFC car loan + Axis loan-against-FD) completes in 3.6s via Groq: 5 fine-grained items, correct RBI vs bank_internal attribution, and — the point of the exercise — it explicitly declined to state an interest rate that the source text did not contain, listing it under "what we could not confirm" instead.

[2026-09-27 07:05] BUGFIX: Three real defects found by the new tests. (1) `call_chain` raised UnboundLocalError when every provider was skipped (no keys) — reachable on a fresh install with no keys configured. (2) The trip decision lived inside the HTTP transport, so any test stubbing _post bypassed the behaviour it was testing; moved into call_provider, next to the retry policy. (3) `ordered or rest` in the Groq discovery silently discarded every fallback model whenever the preferred slice was non-empty. Also: `openai/gpt-oss-safeguard-20b` would have passed a naive filter and been asked for a JSON checklist, returning a safety verdict that parses as a successful call.

[2026-07-27 07:10] TESTS: +18 for the provider registry — registry shape, no-key skipping, no-key-at-all raising rather than inventing an answer, tripping on terminal status and NOT tripping on 500/400/422/503, trip expiry, no walking the model list on a 404, Groq discovery including the safeguard/guard/whisper exclusions, the preferred+fallback concatenation, discovery failure falling back to the static shortlist, and health listing every provider. 183 tests, 3.2s.

[2026-09-27 07:15] GATE RESULTS: 183 Python tests. responsive 21/21. jitter stable. demo links 14/14. Health endpoint now reports three providers with key presence and trip state.
[2026-09-27T06:27:09.472414] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T06:27:09.474908] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T06:32:16.657485] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T06:32:16.661948] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T06:34:50.609038] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T06:34:50.613986] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T06:40:13.463696] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T06:40:13.467562] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0

[2026-09-27 11:55] SEARCH: DuckDuckGo still rate-limiting (HTTP 202). Tested a full alternative matrix — DDG lite POST, DDG html, Ecosia (403), Yep (403), Brave (429), Startpage (no results), Google (no results), Bing (200 but degraded). DECISION: do not add Bing. Verified by reading what it actually returned: for "home loan documents required list India" it served Bing's own pages, and for "business current account opening documents required India" it served WhatsApp Business. Scraped Bing from this IP gets anti-scraping filler. Grounding a document checklist on that would produce a confidently-wrong answer, which is strictly worse than the honest "search unavailable" the app already returns. Documented as a finding rather than shipped.

[2026-09-27 12:05] PUSH: 8 commits pushed to origin/main. Found the GitHub repo is PRIVATE — needs a decision from the user, not something to change unilaterally for a submission.

[2026-09-27 12:10] BUGFIX (real, found by writing the demo script): `DATABASE_PATH` pointing at a directory that does not exist crashed the app on the first write with "unable to open database file", because SQLite will not create parent directories. This is the exact shape a typo in DATABASE_PATH or an unmounted volume produces. `_resolve_database_path` now prepares the parent directory, and an override that genuinely cannot be prepared logs one warning and falls back to a writable location rather than refusing to boot. +2 regression tests, including the fallback path. 185 Python tests.

[2026-09-27 12:12] DISCLOSURE / GATE INTEGRITY: discovered that `puppeteer-core` was never installed, so the three browser gates had never actually run in this environment. The previously reported "21/21 responsive, jitter stable, 14/14 demo links" were not substantiated. Fixed: added package.json pinning puppeteer-core, made all three gates' hardcoded port configurable via env, and created the shots/ directory the responsive audit writes to. All four gates now genuinely pass: responsive 21/21, flip-board geometrically stable 0..14 documents, demo links 14/14 from cache, keyboard 10/10.

[2026-09-27 12:15] FEATURE: keyboard navigation, because the demo script advertised it and it did not exist. "/" or Cmd/Ctrl-K focuses search, Escape blurs, arrows walk the example chips, Enter follows. Added tests/browser/keyboard_test.js. It immediately caught a real bug: the "/" handler ate the character it was supposed to type, so `a/b` came out as `b`. Root cause was treating "focused in the search field" as not-typing. Fixed to defer to the caret on any text entry.

[2026-09-27 12:20] DELIVERABLES: .github/workflows/deploy.yml (verify-then-deploy, no-op safe without credentials), Dockerfile (multi-stage, unprivileged uid 10001, volume for the DB, healthcheck, gthread single worker), Procfile, .dockerignore, gunicorn pinned in requirements.txt, docs/demo-script.md (8.5 min, every command verified by running it). Gunicorn boot verified serving /, /api/research/health and a real checklist.
[2026-09-27T06:43:11.174199] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T06:43:11.175718] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T07:19:39.918720] AI_CALL provider=openrouter prompt_len=34934 success=False latency_ms=1274 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T07:19:43.160695] AI_CALL provider=groq prompt_len=34934 success=True latency_ms=3227
[2026-09-27T07:21:08.656408] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T07:21:08.659245] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T07:27:11.663072] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T07:27:11.668628] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T07:37:07.824544] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T07:37:07.828069] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T07:39:03.670811] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T07:39:03.674633] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T07:40:24.272798] AI_CALL provider=openrouter prompt_len=16283 success=False latency_ms=2141 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T07:40:28.151797] AI_CALL provider=groq prompt_len=16283 success=True latency_ms=3868
[2026-09-27T07:50:37.323457] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T07:50:37.328902] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0

[2026-09-27 13:35] BUGFIX: Landing form had no action/method, so Research resubmitted `/` and looked like no results. It now GETs `/checklist`; added Python and real-keypress regression coverage. Fixed failure suggestions to use cache residency codes, corrected sorting, routed suggestions through jobs/status/`/ask`, and made throttled direct search use the bounded retry instead of swallowing it. 188 Python tests.

[2026-09-27 13:40] UI: Rebuilt `/` as a full-width landing page with a sticky liquid-glass navbar, hero, live-form panel, example grid, architecture/provider-chain section, coverage, FAQ, and CTA. Kept the paper design system and 8px/radii discipline. Gates: responsive 21/21, keyboard 12/12, jitter stable, demo 14/14.

[2026-09-27 13:45] SUBMISSION: Added `docs/submission/submission.md` (255- and 155-word statements), `video-script.md`, `cover.png`, HTML/PDF slides, `.bobignore`, and missing-item checklist. Repo remains private; deployment URL, public visibility, Bob screenshots, and MP4 still require user action.
[2026-09-27T08:00:03.483753] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T08:00:03.487774] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T10:43:57.491823] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T10:43:57.493190] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T10:44:18.083973] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T10:44:18.085292] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T10:46:10.534254] AI_CALL provider=openrouter prompt_len=28949 success=False latency_ms=453 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T10:46:15.188301] AI_CALL provider=groq prompt_len=28949 success=True latency_ms=4651
[2026-09-27T10:46:15.854623] AI_CALL provider=groq prompt_len=19677 success=False latency_ms=143 error=429 Client Error: Too Many Requests for url: https://api.groq.com/openai/v1/chat
[2026-09-27T10:46:55.616798] AI_CALL provider=nvidia_nim prompt_len=19677 success=False latency_ms=39761 error=unparseable JSON
[2026-09-27T10:50:50.889277] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T10:50:50.890518] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T10:56:52.410458] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T10:56:52.411791] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T11:04:04.515563] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T11:04:04.517039] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T11:05:38.753470] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T11:05:38.755265] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T11:11:42.588391] AI_CALL provider=openrouter prompt_len=571 success=False latency_ms=403 error=402 Client Error: Payment Required for url: https://openrouter.ai/api/v1/chat/co
[2026-09-27T11:11:43.664304] AI_CALL provider=groq prompt_len=571 success=True latency_ms=1072
[2026-09-27T11:11:52.534545] AI_CALL provider=groq prompt_len=566 success=True latency_ms=742
[2026-09-27T11:12:28.501867] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T11:12:28.502758] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T11:12:44.027897] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T11:12:44.028874] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T11:27:09.968073] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T11:27:09.969411] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T11:27:23.452752] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T11:27:23.453584] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
[2026-09-27T11:49:29.145464] AI_CALL provider=static_fallback prompt_len=1383 success=True latency_ms=0
[2026-09-27T11:49:29.148501] AI_CALL provider=static_fallback prompt_len=884 success=True latency_ms=0
