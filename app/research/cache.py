"""
Kaagaz — research cache.

One row per canonical (transaction, bank, residency, state) question. The row
is simultaneously the cache and the audit trail: it stores the answer, every
source URL used, when it was researched, and the exact query that produced it.
"""

import json
import os
import sqlite3
import time
from datetime import datetime, timezone

# ── Freshness windows (Section 3) ───────────────────────────────────────────
# Document requirements are slow-moving: what a bank asks for changes on the
# order of months. Interest rates move in weeks. So the two get different TTLs
# and a rate-bearing entry is re-researched far sooner than a document list.
TTL_DOCUMENTS_DAYS = 30
TTL_RATES_DAYS = 7

# A single cache entry is a whole researched answer, and that answer usually
# contains both a document list and rate/fees. We therefore take the SHORTER
# of the two windows for the entry as a whole — a stale rate is worse than a
# slightly stale document list, so the rate window governs.
DEFAULT_TTL_DAYS = TTL_RATES_DAYS

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS research_cache (
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    bank                  TEXT NOT NULL DEFAULT '',
    applicant_residency_status TEXT NOT NULL DEFAULT 'resident',
    loan_or_transaction_type TEXT NOT NULL,
    state                 TEXT NOT NULL DEFAULT '',
    cache_key             TEXT UNIQUE NOT NULL,

    -- the researched payload
    answer_json           TEXT NOT NULL,
    summary               TEXT NOT NULL DEFAULT '',
    interest_rate_range   TEXT,
    processing_fee_note   TEXT,
    regulatory_note       TEXT,

    -- audit trail
    source_urls           TEXT NOT NULL DEFAULT '[]',
    researched_at         TEXT NOT NULL,
    research_query        TEXT NOT NULL DEFAULT '',
    search_query          TEXT NOT NULL DEFAULT '',
    model                 TEXT NOT NULL DEFAULT '',
    provider              TEXT NOT NULL DEFAULT '',
    latency_ms            INTEGER NOT NULL DEFAULT 0,
    cache_ttl_days        INTEGER NOT NULL DEFAULT 7,
    is_seed               INTEGER NOT NULL DEFAULT 0,
    hit_count             INTEGER NOT NULL DEFAULT 0
)
"""

CREATE_INDEX = """
CREATE INDEX IF NOT EXISTS idx_cache_key ON research_cache (cache_key)
"""


def make_cache_key(transaction_type, bank, residency, state):
    """Canonical lookup key. Order is fixed; case/space insensitive upstream."""
    parts = [
        (transaction_type or "").strip().lower(),
        (bank or "").strip().lower(),
        (residency or "resident").strip().lower(),
        (state or "").strip().lower(),
    ]
    return "|".join(parts)


def _connect(app):
    db_path = app.config["DATABASE"]
    conn = sqlite3.connect(db_path, timeout=15)
    conn.row_factory = sqlite3.Row
    return conn


def init_schema(app):
    conn = _connect(app)
    try:
        conn.execute(CREATE_TABLE)
        conn.execute(CREATE_INDEX)
        conn.commit()
    finally:
        conn.close()


def _row_to_dict(row):
    d = dict(row)
    try:
        d["answer"] = json.loads(d.pop("answer_json") or "{}")
    except (ValueError, TypeError):
        d["answer"] = {}
    try:
        d["source_urls"] = json.loads(d.get("source_urls") or "[]")
    except (ValueError, TypeError):
        d["source_urls"] = []
    d["is_seed"] = bool(d.get("is_seed"))
    d["researched_at_epoch"] = _parse_iso_epoch(d.get("researched_at"))
    return d


def _parse_iso_epoch(value):
    if not value:
        return 0.0
    try:
        return datetime.fromisoformat(value).timestamp()
    except (ValueError, TypeError):
        return 0.0


def get_fresh(app, cache_key, max_age_days=None):
    """Return the cached row if it exists and is still inside its TTL.

    Returns None on a miss or on a stale entry — callers then research.
    """
    conn = _connect(app)
    try:
        row = conn.execute(
            "SELECT * FROM research_cache WHERE cache_key = ?", (cache_key,)
        ).fetchone()
    finally:
        conn.close()
    if row is None:
        return None

    entry = _row_to_dict(row)
    ttl = max_age_days if max_age_days is not None else entry["cache_ttl_days"]
    age_days = (time.time() - entry["researched_at_epoch"]) / 86400.0
    if age_days > ttl:
        entry["stale"] = True
        entry["age_days"] = round(age_days, 2)
        return None
    return entry


def get_any(app, cache_key):
    """Return the cached row regardless of age (used to explain staleness)."""
    conn = _connect(app)
    try:
        row = conn.execute(
            "SELECT * FROM research_cache WHERE cache_key = ?", (cache_key,)
        ).fetchone()
    finally:
        conn.close()
    return _row_to_dict(row) if row else None


def store(app, cache_key, *, transaction_type, bank, residency, state,
          answer, source_urls, research_query, search_query, summary="",
          interest_rate_range="", processing_fee_note="", regulatory_note="",
          model="", provider="", latency_ms=0, ttl_days=DEFAULT_TTL_DAYS,
          is_seed=False):
    now = time.time()
    conn = _connect(app)
    try:
        conn.execute(
            """INSERT INTO research_cache
               (bank, applicant_residency_status, loan_or_transaction_type, state,
                cache_key, answer_json, summary, interest_rate_range,
                processing_fee_note, regulatory_note, source_urls, researched_at,
                research_query, search_query, model, provider, latency_ms,
                cache_ttl_days, is_seed, hit_count)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,0)
               ON CONFLICT(cache_key) DO UPDATE SET
                 answer_json=excluded.answer_json,
                 summary=excluded.summary,
                 interest_rate_range=excluded.interest_rate_range,
                 processing_fee_note=excluded.processing_fee_note,
                 regulatory_note=excluded.regulatory_note,
                 source_urls=excluded.source_urls,
                 researched_at=excluded.researched_at,
                 research_query=excluded.research_query,
                 search_query=excluded.search_query,
                 model=excluded.model,
                 provider=excluded.provider,
                 latency_ms=excluded.latency_ms,
                 cache_ttl_days=excluded.cache_ttl_days,
                 is_seed=excluded.is_seed,
                 hit_count=research_cache.hit_count + 1""",
            (
                bank, residency, transaction_type, state, cache_key,
                json.dumps(answer, ensure_ascii=False),
                summary,
                interest_rate_range,
                processing_fee_note,
                regulatory_note,
                json.dumps(list(source_urls), ensure_ascii=False),
                datetime.fromtimestamp(now, timezone.utc).isoformat(),
                research_query,
                search_query,
                model,
                provider,
                int(latency_ms),
                int(ttl_days),
                1 if is_seed else 0,
            ),
        )
        conn.commit()
    finally:
        conn.close()
    return get_any(app, cache_key)


def touch(app, cache_key):
    conn = _connect(app)
    try:
        conn.execute(
            "UPDATE research_cache SET hit_count = hit_count + 1 WHERE cache_key = ?",
            (cache_key,),
        )
        conn.commit()
    finally:
        conn.close()


def stats(app):
    conn = _connect(app)
    try:
        row = conn.execute(
            """SELECT COUNT(*) AS entries,
                      SUM(hit_count) AS hits,
                      SUM(CASE WHEN is_seed = 1 THEN 1 ELSE 0 END) AS seeds,
                      MIN(researched_at) AS oldest,
                      MAX(researched_at) AS newest
               FROM research_cache"""
        ).fetchone()
        sources = conn.execute(
            "SELECT source_urls FROM research_cache"
        ).fetchall()
    finally:
        conn.close()
    urls = set()
    for r in sources:
        try:
            urls.update(json.loads(r["source_urls"] or "[]"))
        except (ValueError, TypeError):
            pass
    return {
        "entries": row["entries"] or 0,
        "hits": row["hits"] or 0,
        "seeds": row["seeds"] or 0,
        "oldest": row["oldest"],
        "newest": row["newest"],
        "distinct_sources": len(urls),
    }


def list_entries(app, limit=200):
    conn = _connect(app)
    try:
        rows = conn.execute(
            """SELECT cache_key, bank, applicant_residency_status,
                      loan_or_transaction_type, state, researched_at,
                      cache_ttl_days, is_seed, hit_count, model
               FROM research_cache
               ORDER BY researched_at DESC
               LIMIT ?""",
            (limit,),
        ).fetchall()
    finally:
        conn.close()
    return [dict(r) for r in rows]
