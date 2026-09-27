#!/usr/bin/env python
"""
Pre-warm the research cache from the researched seed set.

Run this well before recording the demo, and re-run it any time you want to
refresh a stale entry:

    python -m scripts.preseed            # seed anything not already cached
    python -m scripts.preseed --force    # re-seed everything, overwriting
    python -m scripts.preseed --list     # show what is in the cache

The seed entries are real researched answers with real source URLs (see
app/data/seed_research.py). Writing them into research_cache means the app's
normal cache-first path serves them with no code path of their own — the demo
hits exactly the same code as a live query, just faster.
"""

import argparse
import os
import sys
import time
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app                              # noqa: E402
from app.data.seed_research import SEED_ENTRIES          # noqa: E402
from app.research import cache as cache_mod, refdata    # noqa: E402
from app.research.search import build_research_query    # noqa: E402
from app.research.synthesize import NOT_DISCLOSED       # noqa: E402


def seed_all(app, force=False, verbose=True):
    """Write every seed entry into the research cache."""
    cache_mod.init_schema(app)
    now = datetime.now(timezone.utc)

    written = skipped = 0
    for entry in SEED_ENTRIES:
        tx = refdata.normalize_category(entry["transaction_type"])
        bank = refdata.normalize_bank(entry["bank"])
        state = refdata.normalize_state(entry["state"])
        residency = refdata.normalize_residency(entry["residency"])
        key = cache_mod.make_cache_key(tx, bank, residency, state)

        if not force and cache_mod.get_any(app, key) is not None:
            skipped += 1
            if verbose:
                print("  = %-52s already cached" % _label(tx, bank, state))
            continue

        answer = dict(entry)
        answer["sources"] = entry.get("sources", [])
        # Guarantee the shape the live pipeline produces, so seed and live
        # answers render through identical code.
        answer.setdefault("disclosures", [])
        answer.setdefault("regulatory_note", "")
        # step_order is assigned by the live pipeline's normaliser; seeds must
        # carry it too or the stored row is not the same shape.
        answer["items"] = [
            dict(item, step_order=i)
            for i, item in enumerate(entry.get("items", []), start=1)
        ]

        urls = [s["url"] for s in answer["sources"] if s.get("url")]

        cache_mod.store(
            app, key,
            transaction_type=tx,
            bank=bank,
            residency=residency,
            state=state,
            answer=answer,
            source_urls=urls,
            research_query=build_research_query(
                tx, bank, refdata.residency_phrase(residency), state
            ),
            search_query="",
            summary=entry.get("summary", ""),
            interest_rate_range=entry.get("interest_rate_range", ""),
            processing_fee_note=entry.get("processing_fee_note", ""),
            regulatory_note=entry.get("regulatory_note", ""),
            model="seed-research",
            provider="pre-warmed",
            latency_ms=0,
            # Seeds carry the longer document-requirement window: the research
            # is real but deliberately frozen, and document lists move slowly.
            ttl_days=cache_mod.TTL_DOCUMENTS_DAYS,
            is_seed=True,
        )
        written += 1
        if verbose:
            print("  + %-52s %d items, %d sources"
                  % (_label(tx, bank, state), len(entry.get("items", [])), len(urls)))

    return written, skipped


def _label(tx, bank, state):
    bits = [tx]
    if bank:
        bits.append(bank)
    if state:
        bits.append(state)
    return " / ".join(bits)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true",
                    help="overwrite entries that are already cached")
    ap.add_argument("--list", action="store_true",
                    help="print the current cache contents and exit")
    args = ap.parse_args()

    app = create_app()

    if args.list:
        rows = cache_mod.list_entries(app, 500)
        if not rows:
            print("Cache is empty. Run: python -m scripts.preseed")
            return
        print("%-46s %-16s %-22s %-10s %s"
              % ("TRANSACTION", "BANK", "RESIDENCY", "SEED", "RESEARCHED"))
        print("-" * 118)
        for r in rows:
            print("%-46s %-16s %-22s %-10s %s"
                  % (r["loan_or_transaction_type"][:45],
                     (r["bank"] or "-")[:15],
                     r["applicant_residency_status"][:21],
                     "yes" if r["is_seed"] else "live",
                     r["researched_at"][:19].replace("T", " ")))
        return

    print("Pre-warming research cache…")
    started = time.time()
    written, skipped = seed_all(app, force=args.force)
    print()
    print("  seeded %d, already present %d, in %.1fs"
          % (written, skipped, time.time() - started))
    print("  %s" % cache_mod.stats(app))


if __name__ == "__main__":
    main()
