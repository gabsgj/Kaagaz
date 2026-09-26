# Kaagaz — User Needs & Scope

## Problem Statement

In India, routine banking and financial transactions — opening an NRI account, taking a home loan, registering a property sale with a linked loan disbursement, opening a business current account — each require a specific bundle of documents, attestations, stamps, and government forms. This list is scattered across bank websites, RBI circulars, state stamp-duty schedules, and registrar offices, and it is rarely presented in one place, in the right order, with real costs attached.

People find out they're missing something (a notarized affidavit, a specific denomination of adhesive stamp, an apostille) only when they're already at the counter, causing repeat trips, missed appointments, and in some cases financial deadlines being missed entirely.

## Solution

Kaagaz gives a single, ordered, costed checklist for a defined set of transaction types, sourced from a curated dataset built specifically for this project.

## MVP Scope

### Transaction types (exactly these four)
1. Home loan application (salaried applicant)
2. NRI account opening (NRE/NRO)
3. Property sale deed registration with linked bank loan disbursement
4. Business current account opening (proprietorship / partnership / private limited, GST-linked)

### States covered (state-dependent items only)
- Kerala
- Maharashtra
- Data model designed so adding a third state = data entry, not code change

### Explicitly out of scope
- Live document upload / verification
- OCR
- Actual e-stamping integration
- Payment processing
- User accounts / auth beyond simple session
- Multi-language UI (English only; structure copy for i18n later)

## Core features (build priority order)
1. **Transaction picker** — user selects transaction type and (if relevant) state
2. **Checklist generation** — ordered list with: plain-language explanation, how to obtain, approx cost, approx time, dependencies
3. **AI-assisted plain-language layer** — inline AI explainer, grounded on curated dataset (RAG layer)
4. **Progress checklist ("flip board")** — user marks items done; visual split-flap counter
5. **Downloadable/shareable summary** — print-styled page (stretch goal)

## Accuracy constraints
- Never attribute state-level stamp duty rules to RBI
- All AI responses must be grounded in the dataset — no free-form financial/legal claims
- Visible disclaimer: "Kaagaz is an informational prototype, not legal or financial advice"
