# Kaagaz — Decision Log

Append-only. Format: `[YYYY-MM-DD HH:MM] DECISION: ... REASON: ... ALTERNATIVES: ...`

---

[2026-09-25 00:01] DECISION: Primary OpenRouter model = `mistralai/mistral-7b-instruct` (or `openai/gpt-4o-mini` if the former is unavailable). REASON: Fast, cheap, strong instruction-following for short grounded-answer generation; low latency keeps the inline AI explainer snappy. The task is ~200-token grounded Q&A — no need for a larger model. ALTERNATIVES: `anthropic/claude-3-haiku` (good but slightly more expensive), `google/gemma-2-9b-it` (good quality/cost but less reliably instruction-tuned for structured JSON contexts). Logging both as fallback candidates if mistral-7b is unavailable on the OpenRouter account.

[2026-09-25 00:02] DECISION: NVIDIA NIM fallback model = `meta/llama-3.1-8b-instruct`. REASON: Widely available on NIM, strong instruction-following, similar size class to the OpenRouter primary so the fallback behavior is predictable. ALTERNATIVES: `mistralai/mistral-7b-instruct-v0.3` on NIM (also good, but llama-3.1 has better instruction format alignment with the system-prompt pattern we're using).

[2026-09-25 00:03] DECISION: Deployment time-box = 30 minutes on Vercel before falling back to AWS Elastic Beanstalk. REASON: Vercel Flask/WSGI support is well-documented and fast to configure; if it requires >30 min of debugging, EB is more familiar for Python apps. ALTERNATIVES: Fly.io (also fast, but requires Docker familiarity); raw EC2 (too slow under time pressure).

[2026-09-25 00:04] DECISION: SQLite file stored at `instance/kaagaz.db` (Flask instance folder), excluded from git. Seeded at app startup if the file doesn't exist. REASON: Instance folder is the Flask-idiomatic location for runtime-generated files. ALTERNATIVES: In-memory SQLite (faster but loses data on restart, makes debugging harder); Postgres (overkill for MVP).

[2026-09-25 00:05] DECISION: flip-board component implemented as pure vanilla CSS/JS (no npm). Each "card" uses CSS 3D transforms (`rotateX`) with a top-half/bottom-half split. Transitions triggered by JS class toggle. REASON: The stack explicitly has no frontend build step. ALTERNATIVES: Using `@kitlangton/rolling-number` as a CDN script — rejected because it requires a bundler for tree-shaking and its CDN availability is uncertain.

[2026-09-25 00:06] DECISION: AI grounding strategy — pass up to 5 most relevant dataset rows as JSON in the system prompt. Do not use a vector DB for MVP (overkill for <200 rows). Simple keyword match from the user's question against document_name and plain_explanation fields, then pass matching rows. REASON: The dataset is small; semantic search is unnecessary and adds latency + complexity. ALTERNATIVES: chromadb in-process (considered; rejected for complexity); full-text SQLite FTS5 (a reasonable middle ground, adding to backlog if time allows).
