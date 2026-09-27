# Kaagaz submission package

## Project title

Kaagaz — a research agent for Indian banking paperwork

## Short description

Kaagaz turns any Indian banking-document question into an ordered, costed, regulator-aware checklist. It searches the live web, reads sources, cites every claim, and files each answer with its audit trail.

## Long description — Problem & Solution Statement

*255 words; limit: 500.*

Indian banking paperwork fails at the counter, not online. For a home loan, NRI account, property registration, gold loan, Mudra loan, or Kisan Credit Card, the required documents, attestations, stamp duties, fees, and timelines are scattered across bank product pages, RBI circulars, and state registrar notices. Applicants discover a missing affidavit, attestation, stamp, or FEMA declaration during an appointment, causing repeat visits, missed disbursements, and avoidable anxiety. Residents, NRIs, mixed households, and all-NRI borrowers face different requirements, yet most checklists ignore applicant status. Worse, RBI rules and state stamp-duty rules are routinely conflated, sending people to the wrong authority.

Kaagaz is a web research agent for this exact problem. A user describes any transaction in free text, optionally names a bank and state, and selects applicant residency. Kaagaz normalizes the request, returns a fresh cached answer instantly when available, and otherwise researches it live: it searches the web, reads source pages, ranks regulator and bank sources above aggregators, structures the findings into an ordered checklist, and files the answer with its query, timestamp, sources, model, and provider. Every result shows document order, plain-language explanations, costs, timelines, rate bands, regulator attribution, source links, and the exact research record. It refuses to invent figures, never attributes stamp duty to the RBI, and says when a rate is not publicly disclosed.

The approach is creative because coverage is unbounded. Unknown banks and products are researched rather than rejected. Search and generation use independent fallbacks, while fourteen pre-researched cases make demonstrations reliable and search outages show overlapping cached alternatives.

## IBM Bob Usage Statement

*155 words; limit: 500.*

IBM Bob 2.0 was used as an engineering partner throughout Kaagaz, from architecture through final verification. It helped design the cache-first research agent so search and generation could fail independently, preserve evidence, and retain a complete audit trail. It assisted in implementing the OpenRouter-to-Groq-to-NVIDIA NIM provider registry, temporary circuit-breaking for unavailable providers, runtime Groq model discovery, DuckDuckGo search-result parsing, page ranking, SQLite caching, background-job polling, failure suggestions, keyboard navigation, responsive styling, and regression tests.

Bob also helped diagnose concrete defects: a landing-page form that reloaded the home page instead of opening results, residency-code mismatches that emptied failure suggestions, background-thread application-context errors, contrast and mobile-overflow failures, and stale documentation. It proposed focused automated tests for each fix rather than relying on visual inspection.

Kaagaz does not use IBM watsonx.ai or IBM watsonx Orchestrate. The submitted repository contains the Bob-assisted implementation, while screenshots of Bob task-session summaries must be added for each team member before final submission.

## Technology and category tags

- Technologies: Python, Flask, SQLite, Jinja2, JavaScript, HTML, CSS, OpenRouter, Groq, NVIDIA NIM, Puppeteer
- Categories: AI Agents, FinTech, Web Application, Information Retrieval
- Demo platform: Web application

## Links and repository status

- Code repository: `https://github.com/gabsgj/Kaagaz`
- Current visibility: **PRIVATE**
- Required action before submission:
  1. Confirm that `.env` and local databases are untracked.
  2. Run: `gh repo edit gabsgj/Kaagaz --visibility public`
  3. Add IBM Bob task-session summary screenshots for every team member.
- Application URL: **missing until the app is deployed**
- Cover image: `docs/submission/cover.png`
- Slide presentation: `docs/submission/slide-presentation.html` and `docs/submission/slide-presentation.pdf`
- Demonstration video: **missing until recorded**; use `docs/submission/video-script.md`.

## IBM Bob evidence still needed

Create one screenshot per team member showing the IBM Bob task-session summary, then save it under:

- `docs/submission/bob-task-summary-gabriel.png`
- `docs/submission/bob-task-summary-<teammate>.png`

Do not paste API keys, tokens, passwords, or private URLs into screenshots. The repository already ignores `.env`, SQLite files, virtual environments, and generated screenshots through `.gitignore` and `.bobignore`.
