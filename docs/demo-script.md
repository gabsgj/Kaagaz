# Demo script

Eight and a half minutes of runnable, verified material. Every command below
has been run in this repo; the output shown is what it actually printed.

The single most important rule: **everything in Part A works with no keys and
no network.** DuckDuckGo is currently rate-limiting this IP, so any live
demonstration must not depend on it. Part A is the demo. Part B is the
unrehearsed part, and it degrades visibly and honestly.

---

## Part A — the reliable demo (4 min, zero dependencies)

### A1. Cold start on an empty database (30s)

The strongest thing to show: there is no setup step, no seed command, no
migration.

```bash
rm -rf /tmp/demo && DATABASE_PATH=/tmp/demo/kaagaz.db python wsgi.py
```

Open `http://127.0.0.1:5000`. State the obvious thing out loud: *that database
file did not exist four seconds ago.* The schema is created, the cache is
seeded with 14 researched cases, and all of them are answered with no API keys
at all.

This is a real fix, not a flourish. `DATABASE_PATH` pointing into a directory
that doesn't exist used to crash the app on the first write, because SQLite
will not create parent directories. It was found by running the demo script
rather than by reading the code, which is the argument for having one.

### A2. The fully-cited, source-level answer (60s)

Home → **Home loan · HDFC Bank · Indian resident**.

Talk over the thing the app is actually for. Every line is a link. Click two or
three — the official HDFC checklist page, a bank page, an RBI page. Say the
uncomfortable part out loud, because it is the point:

> "This is the RBI floor, not the bank's own list. Where the two differ, the app
> labels it. The LLM does not decide that — it's a code rule in
> `synthesize._fix_state_misattribution`, so it can't be talked out of it."

Then open the **source list** and point at the date and the count. Then open
**Research trail** and show the cache decision. This is the "does it show its
work" requirement, and it is a click, not a promise.

### A3. Honesty about what could not be confirmed (60s)

Home → **Personal loan · Indian resident**.

This is the one to spend time on. The honesty section at the bottom reads:

> "Rate ranges for unsecured lending are wide because the price is set by credit
> score, and the same borrower can be offered very different rates by different
> lenders. The effective cost is the APR, not the headline rate — include
> processing fees, documentation fees and insurance when comparing."

Say the uncomfortable part out loud, because it is the point:

> "This source did not state one rate, so the app did not print one. It said
> *here is why a single number would be a lie, and here is what to compare
> instead.* A chatbot would have produced a confident 12% or 14%, because the
> failure mode of an LLM is to fill gaps rather than admit them."

All 14 cached cases carry this section, so you can navigate to whichever one
suits the moment. Do not rush this — it is the strongest 30 seconds in the demo.

### A4. The registry is real, not a mock (60s)

```bash
curl -s localhost:5000/api/research/health | python3 -m json.tool
```

Point at each provider and its key/trip state, then run:

```bash
python -W ignore -u -c "
from app.ai.client import PROVIDERS
for p in PROVIDERS: print('%-12s key=%-5s models=%d' % (p.name, bool(p.key()), len(p.models)))"
```

> "OpenRouter is tripped — the key is a free tier with no credit, so every call
> opens with a 402. The breaker skips it for five minutes. Groq answers in 0.9
> seconds. This isn't a mock: `app/ai/client.py` walks a real registry and
> discovers Groq's actual model list, because the two models a hardcoded list
> would have named don't exist on this account and 404."

### A5. Coverage is unbounded (30s)

Type an arbitrary combination — any bank, any state, any transaction type. Say
plainly: the 14 cached cases are a safety net, not a catalogue. Anything else
goes out to live search, and the flip-board shows the real stages while it
happens.

### A6. Keyboard, and the failure path (30s)

Press `/` from anywhere — the caret jumps to the search field. Press `Escape` to
leave it, then `ArrowDown` to walk the example chips and `Enter` to follow one.
The `keyboard_test.js` gate asserts all of this on a real keypress path, so if it
looks right here it is right.

Then turn off Wi-Fi and hit a cached case — it still answers instantly and still
cites. Say: *it degraded, and it told you it degraded.*

---

## Part B — the live path (3 min, network required)

**Only attempt this once Part A is banked.** It is the "at least one fully
live, unrehearsed query" requirement, and it depends on a rate limit that is
outside our control.

```bash
python scripts/preseed.py --live "HDFC Flexi personal loan documents" --force
```

If it succeeds, the point is the diff, not the answer: this query was not in the
cache, and the app went out, read real pages, and cited them.

If DuckDuckGo is throttled, **say so and move on.** The app already says
`search_status: unavailable` and falls back to the cache. Explaining a
rate-limited demo in a way that shows you understand the system is worth more
than a green screen you got lucky with.

Recovering from this is just a matter of time — the same code returned 10
results and ranked the official SBI page first when tested earlier today.

---

## Part C — verification (1 min)

```bash
pytest tests/ -q
npm run gates
```

185 Python tests, and four browser gates: responsive 21/21, flip-board stable,
14/14 demo chips, 10/10 keyboard. Say what each gate *proves*, not just that it
is green — the responsive one caught a contrast failure, and the keyboard one
caught a shortcut eating the character it was supposed to type.

---

## If you get asked hard questions

**"Is this just a wrapper on an API?"**
No, and the parts that aren't the wrapper are the parts I wrote. The search
orchestration, the cache and its TTL, the citation provenance, the regulatory
correction, the claim-level honesty gate, the provider registry and breaker,
the cold-start handling, and the tests are all ours. The LLM is a
synthesiser over retrieved text, and every claim is a link to the sentence it
came from.

**"What if the LLM lies?"**
Two layers that don't involve the model. A regex gate rejects unsupported
percentages, and then a validation step retries before giving up. Plus the
retrieval is real: if the text wasn't in the sources, it isn't in the answer.
Ask me to show you the test that breaks it.

**"Why SQLite?"**
One writer, one process, and a file. It's correct for this. The moment it needs
to scale out, that's a migration, and pretending otherwise would be worse than
admitting it.

**"Why is search rate-limited?"**
DuckDuckGo has no public API and rate-limits unofficially. That's the honest
answer, and it's why the app pre-warms a cache, degrades loudly, and never
fabricates to cover a gap.
