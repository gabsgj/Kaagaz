# Kaagaz 3-minute demonstration script

Total: **180 seconds**. At least **120 seconds** show the working solution on screen.

## 0:00–0:20 — Problem

Say:

> “Indian banking paperwork fails at the counter. Home loans, NRI accounts, property registration, gold loans, and Mudra loans all need different documents depending on the bank, state, and applicant. The rules are scattered, and RBI requirements are often confused with state stamp-duty rules.”

Show the Kaagaz landing page while speaking.

## 0:20–0:45 — Ask anything

Type:

- Transaction: `home loan`
- Bank: `HDFC Bank`
- Residency: Resident Indian
- Submit the form.

Say:

> “There is no fixed menu. Unknown banks and products are researched rather than rejected.”

## 0:45–1:40 — Inspect the sourced checklist

Scroll through the cached HDFC home-loan result for at least 55 seconds.

Show:

1. Ordered documents and progress board.
2. Costs, timelines, interest-rate band, and processing fee.
3. RBI, state, registrar, and bank-policy labels.
4. Click at least two source links.
5. Open the exact research record.
6. Mark two documents complete.

Say:

> “Every material claim can be opened. Stamp duty is never labeled as an RBI requirement.”

## 1:40–2:10 — Honesty under missing information

Open Personal Loan and show that an undisclosed rate is reported as a band or explicitly marked unavailable.

Say:

> “Where publication is missing, Kaagaz says so instead of inventing a reassuring number.”

## 2:10–2:35 — Architecture and IBM Bob

Show `/api/research/health`, the provider chain, and the repository files where Bob assisted.

Say:

> “Search and generation fail independently. Providers without keys are skipped, unavailable providers are temporarily removed, and every answer is stored with its sources.”

## 2:35–3:00 — Failure behavior and close

Submit an uncached query, or show the guided failure state with overlapping cached alternatives.

Say:

> “Even an outage remains useful. And everything demonstrated is reproducible through 188 Python tests and four browser gates.”

End on the landing-page architecture section.
