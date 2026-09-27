# Kaagaz — Build Timeline

## Submission deadline
**Sept 27, 2026 — 8:30 PM IST** (20:30 IST)

---

## Phase 1 — foundation (complete)

| Hour | Planned | Actual |
|------|---------|--------|
| 0-1  | Skeleton, .aimem/, config files, dataset curation start | Completed |
| 1-3  | Backend: Flask app, blueprints, SQLite seeding, routes | Completed |
| 3-5  | AI layer: client.py, fallback logic, grounding, prompt templates | Completed |
| 5-8  | Frontend: templates, CSS, flip-board component | Completed |
| 8-10 | Integration: wire all layers, end-to-end test | Completed |
| 10-12| Deployment: Vercel config, env vars, live URL | Completed (config) |
| 12-14| QA: layout check, fallback states, quality bar | Completed |
| 14-16| Docs: README final, submission checklist | Completed |
| 16-48| Buffer: polish, video recording, slides, submission | Carried into Phase 2 |

---

## Phase 2 — visual redesign & data depth (in progress)

Session window: 2026-09-27 01:22 IST → deadline 20:30 IST (~19h).

| Item | Est. | Actual | State |
|------|------|--------|-------|
| Read .aimem, audit Phase 1 build | 0:15 | 0:10 | Done |
| Verify a web-search model is reachable | 0:15 | 0:25 | Done — credit ran out mid-session, see Risks |
| Reference data + normalisation | 0:45 | 0:40 | Done |
| `research_cache` schema + access layer | 0:45 | 0:35 | Done |
| **Research pipeline end-to-end, one example** | 1:30 | 1:10 | **Done — the Section 7 gate.** Live run: 13s, 15 real citations, correct RBI/state split, stored and re-served from cache |
| Job/progress API + graceful degradation | 1:00 | 0:50 | Done |
| Seed research (10 entries, 24 sources) | 1:30 | 1:40 | Done |
| Full CSS rewrite on the 8px scale | 2:00 | 1:50 | Done |
| Custom icon set + collage layer | 1:00 | 0:50 | Done |
| Templates: ask, result, researching, about | 1:30 | 1:30 | Done |
| Flip-board rewrite + jitter gate | 1:00 | 1:10 | Done — machine-verified, 0/14 stable |
| Responsive gate + bug fixing | 1:00 | 1:30 | Done — **21/21 clean**, 8 real bugs fixed |
| Test suite rewrite + green | 1:00 | 1:00 | Done — 133 passing |
| README + .aimem | 0:45 | — | In progress |

### Section 7 scope checklist — state of play

The brief asked for this list to be tracked honestly as it went. Here it is.

1. **Build and fully test the live pipeline end-to-end on one example first.**
   ✅ **Done.** Built and verified *before* any breadth work. Cache miss → web
   search → structured synthesis → stored → re-read from cache, with the whole
   chain exercised on a real query. This is the gate everything else waited on.

2. **Pre-seed the cache for the original seed categories.**
   ✅ **Done, at the minimum the brief asked for.** Ten entries covering home
   loan (resident + NRI), education loan (study abroad, all-NRI), loan against
   FD *and* FD-as-guarantee as a deliberate contrast pair, NRI account, property
   registration (Kerala), business current account, gold loan and Mudra. 24
   distinct primary sources — bank product pages, RBI directions, the Kerala
   Registration Department. All the demo-critical cases hit cache in ~1ms.

3. **Confirm the "ask about anything else" open path works live, correctly, at
   least a few times with different unrehearsed inputs.**
   ⚠️ **Partially done — BLOCKED, needs the user.** The open path was exercised
   live and correctly on three unrehearsed inputs (HDFC home loan in Kerala, SBI
   education loan all-NRI in Karnataka, Bank of Baroda Mudra in Gujarat) *before*
   the OpenRouter free-tier credit ran out mid-session. Every model on the
   account now returns HTTP 402. It has not been re-verified since, because no
   call can be made. **This is the one outstanding item in the whole phase and
   it is blocked on credit, not on code.**

4. **Breadth of pre-seeded content beyond the seed set.**
   ➖ **Deliberately not done, as the brief permits** ("a bonus, not a
   requirement — the architecture itself is what proves unlimited coverage").
   Ten well-sourced entries that demo cleanly beat thirty that are thin.

### One live unrehearsed query in the video (Section 5)

⚠️ **At risk — depends on item 3 above.** The video plan is: pre-warmed examples
from cache, then one live cold query on stage to prove the "ask about anything"
claim. The first half is ready. The second half needs working API credit at
recording time. If credit is unavailable, the fallback is to show the
researching state driven by the real pipeline with the pre-seeded answer landing
— honest, but it does not prove live search to the judges.

---

## Risks, in the order they would hurt

1. **OpenRouter credit exhausted (blocking, needs the user).** `total_credits: 0`;
   every model on the account returns HTTP 402. The live research path is
   implemented, tested and correct, but cannot be *demonstrated* until credit
   exists. ~$5 is enough — a cold research call costs roughly $0.005 and the
   generation step about $0.00005. Note this is also why the seed cache exists
   and is deliberately generous.
2. **Deployment target unverified since Phase 1.** The Vercel config was written
   in Phase 1 but the app has not been deployed or smoke-tested in its Phase 2
   form. The background-thread research job assumes a threaded runtime; the
   polling endpoint has an inline fallback precisely for serverless, but that
   fallback has not been exercised on a real deployment.
3. **Scope creep on seed breadth.** Actively being avoided — see item 4 above.
4. **Video recording time.** Untested. The demo needs a clean cache, a recorded
   fallback for every network step, and one slot reserved for a live query.

## Deliberately not done

- Per-field cache TTLs (the 7-day whole-entry window is the conservative one)
- A dedicated search provider (Tavily/Brave/Serper) — would be a better
  long-term search step than model-native web access, but no key was available;
  it is a drop-in replacement behind `app/research/search.py`
- Document upload, OCR, e-stamping integration, payments, auth, i18n — all
  out of scope per `.aimem/user-needs.md`
