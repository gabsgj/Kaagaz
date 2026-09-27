"""
Kaagaz — Phase 2 tests: research agent, cache, normalisation, routes.

These run with NO network access and NO AI keys. That is deliberate: the tests
assert the things that must be true regardless of whether a search provider is
having a good day — cache correctness, the honesty rules, normalisation, and
the guarantee that no code path renders a blank page.
"""

import json
import os
import re
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app                                  # noqa: E402
from app.research import agent, cache as cache_mod, refdata  # noqa: E402
from app.research.synthesize import (NOT_DISCLOSED, normalize_answer,
                                     _coerce_source)       # noqa: E402
from app.research.search import build_research_query        # noqa: E402


# ══════════════════════════════════════════════════════════════════════
# Normalisation — the layer that makes caching work
# ══════════════════════════════════════════════════════════════════════
class TestNormalisation(unittest.TestCase):

    def test_bank_aliases_collapse_to_one_canonical_name(self):
        for raw in ("sbi", "SBI", "State Bank of India", "state bank of india",
                    "State Bank of India Ltd"):
            self.assertEqual(refdata.normalize_bank(raw),
                             "State Bank of India", raw)

    def test_bank_unknown_passes_through_untouched(self):
        # The whole point of the product: we have never heard of this bank and
        # must still research it rather than reject the question.
        for raw in ("Karnataka Bank", "Some New Co-operative Bank", "ZZZ Bank"):
            self.assertEqual(refdata.normalize_bank(raw), raw)

    def test_state_codes_and_spellings(self):
        for raw in ("kerala", "KL", "Kerala"):
            self.assertEqual(refdata.normalize_state(raw), "Kerala", raw)
        self.assertEqual(refdata.normalize_state("TN"), "Tamil Nadu")
        self.assertEqual(refdata.normalize_state("tamilnadu"), "Tamil Nadu")
        self.assertEqual(refdata.normalize_state("New Delhi"),
                         "Delhi (NCT of Delhi)")
        self.assertEqual(refdata.normalize_state("orissa"), "Odisha")

    def test_state_unknown_passes_through(self):
        self.assertEqual(refdata.normalize_state("Atlantis"), "Atlantis")

    def test_all_36_states_and_uts_present(self):
        self.assertEqual(len(set(refdata.STATES.values())), 36)

    def test_category_aliases(self):
        self.assertEqual(refdata.normalize_category("Home Loan"), "Home loan")
        self.assertEqual(refdata.normalize_category("study abroad loan"),
                         "Education loan (study abroad)")
        self.assertEqual(refdata.normalize_category("FD loan"),
                         "Loan against fixed deposit")
        self.assertEqual(refdata.normalize_category("lap"),
                         "Loan against property")

    def test_category_unknown_passes_through(self):
        weird = "quantum teleportation loan"
        self.assertEqual(refdata.normalize_category(weird), weird)

    def test_residency_enum(self):
        self.assertEqual(refdata.normalize_residency("NRI"), "nri")
        self.assertEqual(refdata.normalize_residency("Non-Resident Indian"),
                         "nri")
        self.assertEqual(refdata.normalize_residency("resident indian"),
                         "resident")
        self.assertEqual(refdata.normalize_residency("all NRIs"), "all_nri")
        self.assertEqual(refdata.normalize_residency("n/a"), "not_applicable")

    def test_residency_values_match_the_schema_enum(self):
        allowed = {"resident", "nri", "mixed_resident_nri", "all_nri",
                   "not_applicable"}
        self.assertTrue(allowed.issubset(set(refdata.RESIDENCY_ORDER)))
        for value in refdata.RESIDENCY_ORDER:
            self.assertIn(refdata.normalize_residency(value), allowed)


# ══════════════════════════════════════════════════════════════════════
# Request parsing
# ══════════════════════════════════════════════════════════════════════
class TestParseRequest(unittest.TestCase):

    def test_missing_transaction_is_the_only_rejection(self):
        with self.assertRaises(agent.ResearchFailed) as ctx:
            agent.parse_request({"bank": "HDFC Bank"})
        self.assertEqual(ctx.exception.kind, "invalid_request")
        self.assertFalse(ctx.exception.retryable)

    def test_unknown_everything_still_produces_a_valid_request(self):
        req = agent.parse_request({
            "transaction_type": "reverse merger loan",
            "bank": "Brand New Bank",
            "state": "Freedonia",
            "residency": "nri",
        })
        self.assertEqual(req["bank"], "Brand New Bank")
        self.assertEqual(req["state"], "Freedonia")
        self.assertEqual(req["residency"], "nri")
        self.assertIn("NRI", req["residency_phrase"])

    def test_residency_canonicalised_when_transaction_cannot_vary(self):
        # Registering a sale deed is the same question for a resident and an NRI.
        for res in ("", "resident", "not_applicable"):
            req = agent.parse_request({
                "transaction_type": "property registration",
                "state": "Kerala",
                "residency": res,
            })
            self.assertEqual(req["residency"], "not_applicable", res)

    def test_explicit_residency_is_still_honoured(self):
        req = agent.parse_request({
            "transaction_type": "property registration",
            "state": "Kerala",
            "residency": "nri",
        })
        self.assertEqual(req["residency"], "nri")

    def test_residency_is_not_canonicalised_where_it_matters(self):
        req = agent.parse_request({
            "transaction_type": "home loan", "residency": "resident",
        })
        self.assertEqual(req["residency"], "resident")

    def test_cache_key_is_order_stable_and_case_insensitive(self):
        a = cache_mod.make_cache_key("Home loan", "HDFC Bank", "resident", "Kerala")
        b = cache_mod.make_cache_key("home loan", "hdfc bank", "RESIDENT", "kerala")
        self.assertEqual(a, b)


# ══════════════════════════════════════════════════════════════════════
# Cache
# ══════════════════════════════════════════════════════════════════════
class TestCache(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.tmp = tempfile.mkdtemp()
        self.app.config['DATABASE'] = os.path.join(self.tmp, 't.db')
        cache_mod.init_schema(self.app)

    def _seed(self, key, **kw):
        return cache_mod.store(
            self.app, key,
            transaction_type=kw.get('tx', 'home loan'),
            bank=kw.get('bank', 'HDFC Bank'),
            residency=kw.get('residency', 'resident'),
            state=kw.get('state', 'Kerala'),
            answer=kw.get('answer', {'items': [], 'sources': []}),
            source_urls=kw.get('urls', ['https://example.com/a']),
            research_query='q', search_query='q',
            model='test', provider='test',
            ttl_days=kw.get('ttl', 7),
            is_seed=kw.get('is_seed', True),
        )

    def test_miss_returns_none(self):
        self.assertIsNone(cache_mod.get_fresh(self.app, 'nothing|here'))

    def test_hit_returns_full_audit_trail(self):
        key = cache_mod.make_cache_key('home loan', 'HDFC Bank', 'resident', 'Kerala')
        self._seed(key, urls=['https://hdfc.example/x', 'https://rbi.example/y'])
        entry = cache_mod.get_fresh(self.app, key)
        self.assertIsNotNone(entry)
        self.assertEqual(entry['source_urls'],
                         ['https://hdfc.example/x', 'https://rbi.example/y'])
        self.assertEqual(entry['research_query'], 'q')
        self.assertTrue(entry['is_seed'])
        self.assertTrue(entry['researched_at'])
        self.assertIn('researched_at_epoch', entry)

    def test_expired_entry_is_a_miss_but_still_retrievable(self):
        key = cache_mod.make_cache_key('old', 'b', 'resident', '')
        self._seed(key, ttl=7)
        conn = cache_mod._connect(self.app)
        conn.execute("UPDATE research_cache SET researched_at = ? "
                     "WHERE cache_key = ?",
                     ('2000-01-01T00:00:00+00:00', key))
        conn.commit()
        conn.close()

        self.assertIsNone(cache_mod.get_fresh(self.app, key),
                          "an entry past its TTL must be a cache miss")
        stale = cache_mod.get_any(self.app, key)
        self.assertIsNotNone(stale, "a stale entry must still be retrievable")
        self.assertTrue(stale['researched_at'].startswith('2000'))

    def test_ttl_windows_are_the_documented_policy(self):
        self.assertEqual(cache_mod.TTL_DOCUMENTS_DAYS, 30)
        self.assertEqual(cache_mod.TTL_RATES_DAYS, 7)
        # The entry as a whole takes the SHORTER window — see decisions.md
        self.assertEqual(cache_mod.DEFAULT_TTL_DAYS, 7)

    def test_store_is_upsert_not_duplicating(self):
        key = cache_mod.make_cache_key('home loan', 'HDFC Bank', 'resident', 'Kerala')
        self._seed(key)
        self._seed(key, answer={'items': [{'document_name': 'new'}], 'sources': []})
        self.assertEqual(cache_mod.stats(self.app)['entries'], 1)
        entry = cache_mod.get_any(self.app, key)
        self.assertEqual(entry['answer']['items'][0]['document_name'], 'new')

    def test_touch_increments_hit_count(self):
        key = cache_mod.make_cache_key('home loan', 'HDFC Bank', 'resident', 'Kerala')
        self._seed(key)
        cache_mod.touch(self.app, key)
        cache_mod.touch(self.app, key)
        self.assertEqual(cache_mod.get_any(self.app, key)['hit_count'], 2)


# ══════════════════════════════════════════════════════════════════════
# Answer normalisation — the honesty rules
# ══════════════════════════════════════════════════════════════════════
class TestAnswerNormalisation(unittest.TestCase):

    def _one_item(self, **over):
        base = {
            "document_name": "Something",
            "plain_explanation": "x",
            "where_to_obtain": "y",
            "approx_cost_min": 100,
            "approx_cost_max": 200,
            "approx_time_days": 3,
            "regulatory_source": "bank_internal",
        }
        base.update(over)
        return base

    def test_rbi_attributed_stamp_duty_is_corrected_in_code(self):
        # The single most important correctness rule in the product.
        answer = normalize_answer({"items": [
            self._one_item(document_name="Stamp duty payment",
                           plain_explanation="Pay stamp duty on the deed",
                           regulatory_source="rbi"),
            self._one_item(document_name="Registration fee at the sub-registrar",
                           plain_explanation="Registration fee payable",
                           regulatory_source="rbi"),
        ]}, [])
        sources = [i["regulatory_source"] for i in answer["items"]]
        self.assertEqual(sources[0], "state_stamp_act")
        self.assertEqual(sources[1], "registrar")

    def test_genuine_rbi_items_are_left_alone(self):
        answer = normalize_answer({"items": [
            self._one_item(document_name="KYC documents",
                           plain_explanation="Know your customer requirements",
                           regulatory_source="rbi"),
        ]}, [])
        self.assertEqual(answer["items"][0]["regulatory_source"], "rbi")

    def test_invalid_regulatory_source_falls_back_by_content(self):
        self.assertEqual(_coerce_source({"regulatory_source": "banana",
                                         "plain_explanation": "KYC norms"}), "rbi")
        self.assertEqual(_coerce_source({"regulatory_source": "",
                                         "plain_explanation": "stamp duty"}),
                         "state_stamp_act")

    def test_inverted_cost_range_is_repaired(self):
        answer = normalize_answer({"items": [
            self._one_item(approx_cost_min=900, approx_cost_max=100),
        ]}, [])
        item = answer["items"][0]
        self.assertLessEqual(item["approx_cost_min"], item["approx_cost_max"])

    def test_absurd_values_are_clamped_or_dropped_not_invented(self):
        answer = normalize_answer({"items": [
            self._one_item(approx_cost_min="not a number",
                           approx_cost_max="₹ 4,000",
                           approx_time_days=99999),
        ]}, [])
        item = answer["items"][0]
        self.assertIsNone(item["approx_cost_min"])
        self.assertEqual(item["approx_cost_max"], 4000)
        self.assertEqual(item["approx_time_days"], 365)

    def test_dangling_dependency_is_dropped_not_rendered(self):
        answer = normalize_answer({"items": [
            self._one_item(document_name="Sale deed"),
            self._one_item(document_name="Encumbrance certificate",
                           depends_on="A document that does not exist"),
        ]}, [])
        self.assertEqual(answer["items"][1]["depends_on"], "")

    def test_resolvable_dependency_is_kept(self):
        answer = normalize_answer({"items": [
            self._one_item(document_name="Sale deed"),
            self._one_item(document_name="Encumbrance certificate",
                           depends_on="sale deed"),
        ]}, [])
        self.assertEqual(answer["items"][1]["depends_on"], "sale deed")

    def test_items_without_a_name_are_discarded(self):
        answer = normalize_answer({"items": [
            {"plain_explanation": "nameless"},
            self._one_item(document_name="Real one"),
        ]}, [])
        self.assertEqual(answer["total"] if "total" in answer else len(answer["items"]), 1)

    def test_answer_with_no_items_is_rejected_so_caller_degrades(self):
        self.assertIsNone(normalize_answer({"items": []}, []))
        self.assertIsNone(normalize_answer({"items": "not a list"}, []))
        self.assertIsNone(normalize_answer("not a dict", []))

    def test_sources_are_carried_onto_the_answer(self):
        citations = [{"url": "https://sbi.bank.in/x", "title": "SBI"}]
        answer = normalize_answer({"items": [self._one_item()]}, citations)
        self.assertEqual(answer["sources"], citations)


# ══════════════════════════════════════════════════════════════════════
# Research query construction
# ══════════════════════════════════════════════════════════════════════
class TestResearchQuery(unittest.TestCase):

    def test_query_names_transaction_bank_state_and_residency(self):
        q = build_research_query("Home loan", "HDFC Bank",
                                 "a resident Indian applicant", "Kerala")
        for fragment in ("Home loan", "HDFC Bank", "Kerala", "resident Indian"):
            self.assertIn(fragment, q)

    def test_query_omits_blank_optionals_rather_than_saying_none(self):
        q = build_research_query("Gold loan", "", "", "")
        self.assertNotIn(" at  ", q)
        self.assertNotIn(" in  ", q)

    def test_query_demands_a_band_and_citations(self):
        q = build_research_query("Personal loan", "ICICI Bank", "an NRI", "")
        self.assertIn("band", q.lower())
        self.assertIn("Cite", q)


# ══════════════════════════════════════════════════════════════════════
# Agent orchestration
# ══════════════════════════════════════════════════════════════════════
class TestAgent(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.tmp = tempfile.mkdtemp()
        self.app.config['DATABASE'] = os.path.join(self.tmp, 't.db')
        cache_mod.init_schema(self.app)

    def test_cache_hit_short_circuits_without_any_network_call(self):
        key = cache_mod.make_cache_key("Home loan", "HDFC Bank", "resident", "")
        cache_mod.store(
            self.app, key,
            transaction_type="Home loan", bank="HDFC Bank",
            residency="resident", state="",
            answer={"summary": "s", "items": [{"document_name": "PAN"}],
                    "sources": []},
            source_urls=[], research_query="q", search_query="q",
            ttl_days=7, is_seed=True,
        )

        import app.research.agent as agent_mod

        def explode(*a, **kw):
            raise AssertionError("cache hit must not touch the network")

        original = agent_mod.search
        agent_mod.search = explode
        try:
            result = agent.answer(self.app, {
                "transaction_type": "home loan", "bank": "HDFC Bank",
                "residency": "resident",
            })
        finally:
            agent_mod.search = original

        self.assertEqual(result['cache'], 'hit')
        self.assertEqual(result['total'], 1)
        self.assertTrue(result['as_of'])

    def test_stale_entry_is_served_labelled_rather_than_erroring(self):
        """A search outage must not strand someone who needs the answer now."""
        key = cache_mod.make_cache_key("Home loan", "HDFC Bank", "resident", "")
        cache_mod.store(
            self.app, key,
            transaction_type="Home loan", bank="HDFC Bank",
            residency="resident", state="",
            answer={"summary": "old", "items": [{"document_name": "PAN"}],
                    "sources": []},
            source_urls=[], research_query="q", search_query="q",
            ttl_days=7, is_seed=True,
        )
        conn = cache_mod._connect(self.app)
        conn.execute("UPDATE research_cache SET researched_at='2000-01-01T00:00:00+00:00' "
                     "WHERE cache_key=?", (key,))
        conn.commit()
        conn.close()

        import app.research.agent as agent_mod
        from app.research.search import SearchError

        def fail(*a, **kw):
            raise SearchError("provider is down")

        original = agent_mod.search
        agent_mod.search = fail
        try:
            result = agent.answer(self.app, {
                "transaction_type": "home loan", "bank": "HDFC Bank",
                "residency": "resident",
            })
        finally:
            agent_mod.search = original

        self.assertEqual(result['cache'], 'stale')
        self.assertTrue(result['stale'])
        self.assertIn('unavailable', result['degraded'].lower())

    def test_search_outage_with_no_cache_raises_a_typed_failure(self):
        import app.research.agent as agent_mod
        from app.research.search import SearchError

        def fail(*a, **kw):
            raise SearchError("provider is down")

        original = agent_mod.search
        agent_mod.search = fail
        try:
            with self.assertRaises(agent.ResearchFailed) as ctx:
                agent.answer(self.app, {"transaction_type": "unheard of loan"})
        finally:
            agent_mod.search = original
        self.assertEqual(ctx.exception.kind, "search_unavailable")
        self.assertTrue(ctx.exception.retryable)
        # The message must be human, never a raw exception.
        self.assertNotIn("Traceback", ctx.exception.message)
        self.assertNotIn("SearchError", ctx.exception.message)

    def test_search_outage_suggests_overlapping_cached_cases(self):
        import app.research.agent as agent_mod
        from app.research.search import SearchError

        for tx in ("Zebra loan", "Alpha loan"):
            cache_mod.store(
                self.app,
                cache_mod.make_cache_key(tx, "Test Bank", "resident", ""),
                transaction_type=tx, bank="Test Bank",
                residency="resident", state="",
                answer={"summary": "s", "items": [], "sources": []},
                source_urls=[], research_query="q", search_query="q",
                ttl_days=7, is_seed=True,
            )

        def fail(*a, **kw):
            raise SearchError("provider is down")

        original = agent_mod.search
        agent_mod.search = fail
        try:
            with self.assertRaises(agent.ResearchFailed) as ctx:
                agent.answer(self.app, {
                    "transaction_type": "Something unheard of",
                    "bank": "Test Bank",
                    "residency": "resident",
                })
        finally:
            agent_mod.search = original

        suggestions = ctx.exception.suggestions
        self.assertEqual(
            [s["transaction_type"] for s in suggestions],
            ["Alpha loan", "Zebra loan"],
        )
        self.assertTrue(suggestions[0]["href"].startswith("/checklist?"))
        self.assertIn("transaction_type=Alpha%20loan", suggestions[0]["href"])
        self.assertIn("Test Bank", suggestions[0]["label"])

    def test_synthesis_failure_degrades_to_sourced_prose_not_a_blank(self):
        import app.research.agent as agent_mod

        FAKE_FINDINGS = "Here is the researched answer with sources."
        FAKE_CITATIONS = [{"url": "https://bank.example/doc", "title": "Bank"}]

        def FakeFound():
            return {"findings": FAKE_FINDINGS, "citations": FAKE_CITATIONS,
                    "model": "fake", "query": "q", "provider": "test",
                    "latency_ms": 1, "searched_at": "2026-09-27T00:00:00"}

        original_search, original_synth = agent_mod.search, agent_mod.synthesize
        agent_mod.search = lambda *a, **kw: FakeFound()
        agent_mod.synthesize = lambda *a, **kw: {"answer": None,
                                                "provider": "none", "model": ""}
        try:
            result = agent.answer(self.app, {
                "transaction_type": "obscure loan", "bank": "Nowhere Bank",
            })
        finally:
            agent_mod.search, agent_mod.synthesize = original_search, original_synth

        self.assertEqual(result['cache'], 'miss')
        self.assertGreaterEqual(result['total'], 1)
        self.assertIn('degraded', result)
        self.assertTrue(result['sources'])

    def test_full_miss_path_persists_everything_for_the_audit_trail(self):
        import app.research.agent as agent_mod

        def FakeFound():
            return {"findings": "notes",
                    "citations": [{"url": "https://a.example/1", "title": "A"},
                                  {"url": "https://b.example/2", "title": "B"}],
                    "model": "fake-search-model", "query": "the exact query",
                    "provider": "test", "latency_ms": 1,
                    "searched_at": "2026-09-27T00:00:00"}

        class FakeSyn:
            answer = {"summary": "sum", "items": [
                          {"step_order": 1, "document_name": "PAN",
                           "plain_explanation": "e", "where_to_obtain": "w",
                           "approx_cost_min": 0, "approx_cost_max": 0,
                           "approx_time_days": 1,
                           "regulatory_source": "rbi", "depends_on": "",
                           "source_note": "s"}],
                      "interest_rate_range": "8% - 9% p.a.",
                      "processing_fee_note": "1%",
                      "regulatory_note": "n", "disclosures": [],
                      "sources": [{"url": "https://a.example/1", "title": "A"}]}

        original_search, original_synth = agent_mod.search, agent_mod.synthesize
        agent_mod.search = lambda *a, **kw: FakeFound()
        agent_mod.synthesize = lambda *a, **kw: {"answer": FakeSyn.answer,
                                                "provider": "openrouter",
                                                "model": "gpt-4o-mini"}
        try:
            result = agent.answer(self.app, {
                "transaction_type": "quantum loan", "bank": "ZZZ Bank",
                "state": "Freedonia", "residency": "nri",
            })
        finally:
            agent_mod.search, agent_mod.synthesize = original_search, original_synth

        stored = cache_mod.get_any(
            self.app,
            cache_mod.make_cache_key("quantum loan", "ZZZ Bank", "nri", "Freedonia"))
        self.assertIsNotNone(stored, "a research result must be written to the cache")
        self.assertEqual(stored['source_urls'],
                         ['https://a.example/1', 'https://b.example/2'])
        self.assertEqual(stored['research_query'], "the exact query")
        self.assertEqual(stored['model'], "fake-search-model")
        self.assertTrue(stored['researched_at'])
        self.assertFalse(stored['is_seed'])
        self.assertEqual(result['cache'], 'miss')

    def test_second_identical_request_hits_the_cache(self):
        import app.research.agent as agent_mod

        calls = {'n': 0}

        def FakeFound():
            return {"findings": "notes",
                    "citations": [{"url": "https://a.example/1", "title": "A"}],
                    "model": "m", "query": "q", "provider": "test",
                    "latency_ms": 1, "searched_at": "2026-09-27T00:00:00"}

        def counting_search(*a, **kw):
            calls['n'] += 1
            return FakeFound()

        class FakeSyn:
            answer = {"summary": "s", "items": [
                {"step_order": 1, "document_name": "PAN", "plain_explanation": "",
                 "where_to_obtain": "", "approx_cost_min": None,
                 "approx_cost_max": None, "approx_time_days": None,
                 "regulatory_source": "rbi", "depends_on": "", "source_note": ""}],
                "sources": []}

        original_search, original_synth = agent_mod.search, agent_mod.synthesize
        agent_mod.search = counting_search
        agent_mod.synthesize = lambda *a, **kw: {"answer": FakeSyn.answer,
                                                "provider": "p", "model": ""}
        try:
            first = agent.answer(self.app, {"transaction_type": "cache test loan"})
            second = agent.answer(self.app, {"transaction_type": "cache test loan"})
        finally:
            agent_mod.search, agent_mod.synthesize = original_search, original_synth

        self.assertEqual(first['cache'], 'miss')
        self.assertEqual(second['cache'], 'hit')
        self.assertEqual(calls['n'], 1, "second request must not re-research")


# ══════════════════════════════════════════════════════════════════════
# Seed data integrity
# ══════════════════════════════════════════════════════════════════════
class TestSeedData(unittest.TestCase):

    def setUp(self):
        from app.data.seed_research import SEED_ENTRIES
        self.entries = SEED_ENTRIES

    def test_seed_set_is_substantial_enough_to_demo(self):
        self.assertGreaterEqual(len(self.entries), 8)

    def test_every_entry_has_real_source_urls(self):
        for entry in self.entries:
            self.assertTrue(entry.get('sources'), entry['transaction_type'])
            for source in entry['sources']:
                self.assertTrue(source['url'].startswith('https://'), source)
                self.assertTrue(source.get('title'), source['url'])

    def test_every_entry_covers_the_two_awkward_distinctions(self):
        # Section 2: these are the two places users most often get confused,
        # so the seed set must demonstrate both.
        residencies = {e['residency'] for e in self.entries}
        self.assertIn('nri', residencies)
        self.assertIn('all_nri', residencies)
        self.assertIn('not_applicable', residencies)

        categories = ' '.join(e['transaction_type'].lower() for e in self.entries)
        self.assertIn('fixed deposit', categories)
        self.assertIn('guarantee', categories)

    def test_no_seed_quote_says_something_went_unpublished_as_a_number(self):
        for entry in self.entries:
            band = entry.get('interest_rate_range', '')
            if 'not publicly disclosed' in band.lower():
                self.assertNotIn('%', band.replace('Not publicly disclosed as a band', ''),
                                 entry['transaction_type'])

    def test_state_stamp_entries_are_never_attributed_to_rbi(self):
        for entry in self.entries:
            if entry['state']:
                for item in entry['items']:
                    blob = (item['document_name'] + ' ' +
                            item.get('plain_explanation', '')).lower()
                    if 'stamp duty' in blob or 'adhesive stamp' in blob:
                        self.assertNotEqual(
                            item['regulatory_source'], 'rbi',
                            "%s: %s" % (entry['transaction_type'],
                                        item['document_name']))

    def test_every_item_has_a_where_and_a_name(self):
        for entry in self.entries:
            for item in entry['items']:
                self.assertTrue(item['document_name'].strip())
                self.assertTrue(item['where_to_obtain'].strip())
                self.assertIn(item['regulatory_source'],
                              {'rbi', 'state_stamp_act', 'registrar',
                               'bank_internal'})

    def test_checklists_are_fine_grained_not_umbrella_rows(self):
        for entry in self.entries:
            names = ' '.join(i['document_name'].lower() for i in entry['items'])
            for umbrella in ("income documents", "property documents",
                             "other documents", "kYC documents"):
                self.assertNotIn(
                    umbrella, names,
                    "%s has an umbrella row '%s' instead of real documents"
                    % (entry['transaction_type'], umbrella))


# ══════════════════════════════════════════════════════════════════════
# Routes
# ══════════════════════════════════════════════════════════════════════
class TestRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from scripts.preseed import seed_all
        cls.app = create_app()
        seed_all(cls.app, force=True, verbose=False)

    def setUp(self):
        self.c = self.app.test_client()

    def test_ask_page_renders_with_reference_data(self):
        r = self.c.get('/')
        self.assertEqual(r.status_code, 200)
        html = r.data.decode()
        self.assertIn('Research it', html)
        self.assertIn('HDFC Bank', html)
        self.assertIn('Kerala', html)
        self.assertIn('Non-Resident Indian', html)

    def test_about_page_explains_both_confusions(self):
        html = self.c.get('/about').data.decode()
        self.assertIn('Loan against FD vs FD as a guarantee', html)
        self.assertIn('resident', html.lower())
        self.assertIn('NRI', html)

    def test_cached_question_renders_a_full_checklist(self):
        r = self.c.get('/checklist?transaction_type=home+loan&bank=HDFC+Bank'
                       '&residency=resident')
        self.assertEqual(r.status_code, 200)
        html = r.data.decode()
        self.assertIn('Documents ready', html)
        self.assertIn('step__num', html)
        self.assertIn('hdfc.bank.in', html)          # real source URL shown
        self.assertIn('Researched', html)             # "as of" provenance
        self.assertIn('Sources read for this answer', html)

    def test_cached_question_shows_the_research_record(self):
        html = self.c.get('/checklist?transaction_type=gold+loan'
                          '&bank=State+Bank+of+India').data.decode()
        self.assertIn('Show the exact research record', html)
        self.assertIn('Researched', html)
        # the cache key is the canonical tx|bank|residency|state tuple
        self.assertIn('gold loan|state bank of india|resident|', html.lower())

    def test_regulatory_legend_and_attribution_are_present(self):
        html = self.c.get('/checklist?transaction_type=property+registration'
                          '&state=Kerala').data.decode()
        for label in ('RBI rules', 'State stamp act', "Registrar / state",
                      "Bank policy"):
            self.assertIn(label, html)
        self.assertIn('data-source="state_stamp_act"', html)
        self.assertIn('step__gov-mark', html)

    def test_uncached_question_serves_the_researching_view(self):
        html = self.c.get('/checklist?transaction_type=inversekite+blender+loan'
                          '&bank=Nowhere+Bank').data.decode()
        self.assertIn('board--working', html)
        self.assertIn('Not in the cache', html)
        self.assertIn('data-ticker-text', html)
        self.assertIn('researchFailed', html)

    def test_empty_transaction_never_renders_a_blank_page(self):
        r = self.c.get('/checklist?transaction_type=&bank=x')
        self.assertEqual(r.status_code, 400)
        body = r.data.decode()
        self.assertIn('Tell us what you', body)
        self.assertIn('Research it', body)

    def test_no_lorem_ipsum_or_placeholder_copy_anywhere(self):
        for url in ('/', '/about',
                    '/checklist?transaction_type=home+loan&bank=HDFC+Bank'):
            html = self.c.get(url).data.decode().lower()
            for junk in ('lorem ipsum', 'dolor sit amet', 'tbd', 'todo',
                         'coming soon', 'xxx', 'placeholder text',
                         'undefined', 'none none'):
                self.assertNotIn(junk, html, "%s in %s" % (junk, url))

    def test_no_gradient_or_blurple_decoration_survives(self):
        for url in ('/', '/about',
                    '/checklist?transaction_type=home+loan&bank=HDFC+Bank'):
            html = self.c.get(url).data.decode().lower()
            self.assertNotIn('linear-gradient(135deg', html)
            self.assertNotIn('#7f5af0', html)   # the archetypal hackathon purple
            self.assertNotIn('#8b5cf6', html)
            self.assertNotIn('blob', html)

    def test_options_endpoint_serves_reference_data(self):
        data = json.loads(self.c.get('/api/research/options').data)
        self.assertIn('banks', data)
        self.assertIn('states', data)
        self.assertEqual(len(data['residency']), 5)
        self.assertGreater(len(data['banks']), 50)

    def test_cache_endpoints(self):
        stats = json.loads(self.c.get('/api/research/cache').data)
        self.assertGreaterEqual(stats['entries'], 10)
        self.assertGreater(stats['distinct_sources'], 15)
        entries = json.loads(self.c.get('/api/research/entries').data)
        self.assertEqual(len(entries), stats['entries'])

    def test_start_endpoint_rejects_an_empty_transaction(self):
        r = self.c.post('/api/research/start', json={'transaction_type': ''})
        self.assertEqual(r.status_code, 400)
        self.assertIn('error', json.loads(r.data))

    def test_status_endpoint_404s_an_unknown_job(self):
        self.assertEqual(self.c.get('/api/research/status/nope').status_code, 404)

    def test_ask_endpoint_returns_a_typed_error_not_a_stack_trace(self):
        r = self.c.post('/api/research/ask', json={'transaction_type': ''})
        self.assertEqual(r.status_code, 503)
        body = json.loads(r.data)
        self.assertIn('error', body)
        self.assertNotIn('Traceback', body['error'])

    def test_static_assets_are_served(self):
        for path in ('/static/css/main.css', '/static/js/flipboard.js',
                     '/static/js/checklist.js', '/static/favicon.svg'):
            self.assertEqual(self.c.get(path).status_code, 200, path)


# ══════════════════════════════════════════════════════════════════════
# Demo reliability
#
# The demo is pre-warmed precisely so the recorded run hits the cache. A seed
# whose example link misses is a broken demo, and that is exactly what happened
# once: the education-loan seed was keyed under "education loan (study abroad)"
# while its example chip asked for "education loan". These tests make that
# class of mistake impossible to reintroduce silently.
# ══════════════════════════════════════════════════════════════════════
def _qs(tx, bank, residency, state):
    parts = ['transaction_type=' + tx.replace(' ', '+'),
             'bank=' + bank.replace(' ', '+'),
             'residency=' + residency]
    if state:
        parts.append('state=' + state.replace(' ', '+'))
    return '/checklist?' + '&'.join(parts)


class TestDemoIsPreWarmed(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        from scripts.preseed import seed_all
        cls.app = create_app()
        seed_all(cls.app, force=True, verbose=False)
        cls.c = cls.app.test_client()

    def test_every_example_chip_serves_from_cache(self):
        from app.checklist.routes import EXAMPLES
        from app.research import agent
        from app.research.cache import make_cache_key

        for tx, bank, residency, state, label, _note in EXAMPLES:
            req = agent.parse_request({
                'transaction_type': tx, 'bank': bank,
                'residency': residency, 'state': state,
            })
            key = make_cache_key(req['transaction_type'], req['bank'],
                                 req['residency'], req['state'])
            with self.subTest(example=label):
                self.assertIsNotNone(
                    cache_mod.get_any(self.app, key),
                    "%r does not resolve to a pre-warmed entry — the demo "
                    "would hit the research path for a case meant to be "
                    "instant" % label,
                )

    def test_every_example_chip_renders_a_checklist_over_http(self):
        from app.checklist.routes import EXAMPLES
        for tx, bank, residency, state, label, _note in EXAMPLES:
            with self.subTest(example=label):
                r = self.c.get(_qs(tx, bank, residency, state))
                self.assertEqual(r.status_code, 200, label)
                self.assertIn(b'Documents ready', r.data, label)
                self.assertNotIn(b'board--working', r.data,
                                 "%r fell through to the researching view" % label)

    def test_domestic_and_study_abroad_education_loans_are_distinct(self):
        """A study-abroad loan is a different product and must not share a key."""
        domestic = refdata.normalize_category('education loan')
        abroad = refdata.normalize_category('study abroad loan')
        self.assertNotEqual(domestic, abroad)
        self.assertEqual(abroad, 'Education loan (study abroad)')
        self.assertEqual(refdata.normalize_category('education loan (study abroad)'),
                         abroad)

    def test_cache_serves_everything_even_with_no_search_provider(self):
        """The app must be fully demonstrable from cache alone.

        This is the property that makes the demo safe: with no API credit at
        all, every pre-warmed case still answers instantly and no code path
        reaches the network.
        """
        from app.checklist.routes import EXAMPLES
        for tx, bank, residency, state, label, _note in EXAMPLES:
            with self.subTest(example=label):
                r = self.c.get(_qs(tx, bank, residency, state))
                self.assertIn(b'Sources read for this answer', r.data, label)


# ══════════════════════════════════════════════════════════════════════
# Deployment
#
# The Phase-1 Vercel config would have taken the app down on its first write:
# the deployment bundle is read-only and only /tmp is writable. These tests
# pin the behaviour that a cold serverless start has to have.
# ══════════════════════════════════════════════════════════════════════
class TestDeployment(unittest.TestCase):

    def _fresh_app(self, tmpdir):
        """An app pointed at a brand-new database, as on a cold start."""
        import importlib
        import app as app_pkg
        previous = os.environ.get('DATABASE_PATH')
        os.environ['DATABASE_PATH'] = os.path.join(tmpdir, 'kaagaz.db')
        try:
            importlib.reload(app_pkg)
            application = app_pkg.create_app()
        finally:
            if previous is None:
                os.environ.pop('DATABASE_PATH', None)
            else:
                os.environ['DATABASE_PATH'] = previous
        return application

    def test_database_path_override_is_honoured(self):
        with tempfile.TemporaryDirectory() as tmp:
            app = self._fresh_app(tmp)
            self.assertEqual(app.config['DATABASE'],
                             os.path.join(tmp, 'kaagaz.db'))
            self.assertTrue(app.config['DATABASE_IS_EPHEMERAL'],
                            "a path outside instance/ does not survive a restart")

    def test_database_path_parent_directory_is_created(self):
        """A DATABASE_PATH whose directory does not exist must still boot.

        SQLite will not create missing parent directories, so returning such a
        path made the very first write fail with "unable to open database file"
        and the app 500'd on boot. This is the shape a typo in DATABASE_PATH or
        a volume that has not been mounted yet produces, which is exactly the
        situation the override exists to handle.
        """
        with tempfile.TemporaryDirectory() as tmp:
            # A directory two levels deep that does not exist yet.
            nested_dir = os.path.join(tmp, 'data', 'sub')
            app = self._fresh_app(nested_dir)
            nested = os.path.join(nested_dir, 'kaagaz.db')
            self.assertEqual(app.config['DATABASE'], nested)
            self.assertTrue(os.path.isdir(os.path.dirname(nested)),
                            'the parent directory should have been created')
            # And it is actually usable, not merely created.
            client = app.test_client()
            self.assertEqual(client.get('/').status_code, 200)
            self.assertEqual(client.get('/api/research/health').status_code, 200)

    def test_unusable_database_path_falls_back_instead_of_crashing(self):
        """An override that cannot be prepared must not stop the app booting.

        A path under a read-only or nonexistent parent is a legitimate
        misconfiguration. The right response is to log it once and fall back to
        a writable location, so the process serves requests and reports its own
        degraded state — not to refuse to start.
        """
        import app as app_pkg
        with tempfile.TemporaryDirectory() as tmp:
            unusable = os.path.join(tmp, 'ro', 'nested', 'kaagaz.db')
            # Make the parent un-creatable by parking a *file* where a
            # directory would have to go.
            os.makedirs(os.path.join(tmp, 'ro'), exist_ok=True)
            with open(os.path.join(tmp, 'ro', 'nested'), 'w') as fh:
                fh.write('not a directory')
            previous = os.environ.get('DATABASE_PATH')
            os.environ['DATABASE_PATH'] = unusable
            try:
                import importlib
                importlib.reload(app_pkg)
                app = app_pkg.create_app()
            finally:
                if previous is None:
                    os.environ.pop('DATABASE_PATH', None)
                else:
                    os.environ['DATABASE_PATH'] = previous
            self.assertNotEqual(app.config['DATABASE'], unusable)
            self.assertEqual(app.test_client().get('/').status_code, 200)

    def test_cold_start_creates_every_table(self):
        """A brand-new database must come up fully schema'd.

        The database-path resolution added for serverless probed the target
        file for writability, which created it. `db_seed` then saw a file that
        already existed, concluded it had been seeded, and returned without
        creating a single table — so a fresh clone started with no
        `checklist_items` table and 500'd on the first checklist page, while
        every research-side test still passed because `init_schema` runs
        unconditionally. This asserts the whole schema, not just the part the
        research path happens to use.
        """
        import sqlite3
        with tempfile.TemporaryDirectory() as tmp:
            app = self._fresh_app(tmp)
            path = app.config['DATABASE']
            self.assertTrue(os.path.exists(path),
                            "the database file should be created by seeding, "
                            "not by the writability probe")
            conn = sqlite3.connect(path)
            tables = {r[0] for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'")}
            conn.close()
            self.assertIn('research_cache', tables)
            self.assertIn('checklist_items', tables)

    def test_cold_start_seed_populates_the_legacy_dataset(self):
        """The Phase-1 static dataset must still be seeded on a fresh database.

        It backs the inline per-document explainer and the graceful-degradation
        path, so an empty table there is a silent loss of a working feature.
        """
        import sqlite3
        with tempfile.TemporaryDirectory() as tmp:
            app = self._fresh_app(tmp)
            conn = sqlite3.connect(app.config['DATABASE'])
            rows = conn.execute(
                "SELECT COUNT(*) FROM checklist_items").fetchone()[0]
            conn.close()
            self.assertGreater(rows, 20,
                               "legacy checklist dataset was not seeded")

    def test_writability_probe_does_not_create_the_database(self):
        """_resolve_database_path must not have the side effect of creating the
        file it is about to hand out. See the note on _is_writable_dir."""
        import importlib
        import app as app_pkg
        with tempfile.TemporaryDirectory() as tmp:
            instance = os.path.join(tmp, 'instance')
            os.makedirs(instance)
            target = os.path.join(instance, 'kaagaz.db')
            saved = os.environ.get('DATABASE_PATH')
            os.environ.pop('DATABASE_PATH', None)
            try:
                importlib.reload(app_pkg)
                path = app_pkg._resolve_database_path(instance)
                self.assertEqual(path, target)
                self.assertFalse(os.path.exists(target),
                                 "probing for writability must not create "
                                 "the database file")
            finally:
                if saved is not None:
                    os.environ['DATABASE_PATH'] = saved
                importlib.reload(app_pkg)

    def test_cold_start_auto_seeds_the_research_cache(self):
        """A cold serverless instance must not answer every question with a
        15-40 second research call."""
        from app.checklist.routes import EXAMPLES
        with tempfile.TemporaryDirectory() as tmp:
            app = self._fresh_app(tmp)
            c = app.test_client()

            health = json.loads(c.get('/api/research/health').data)
            self.assertTrue(health['ok'])
            self.assertGreaterEqual(health['cache']['entries'], 8,
                                    "cold start must rebuild the cache from "
                                    "the bundled seed set")

            for tx, bank, residency, state, label, _note in EXAMPLES:
                with self.subTest(example=label):
                    r = c.get(_qs(tx, bank, residency, state))
                    self.assertEqual(r.status_code, 200, label)
                    self.assertIn(b'Documents ready', r.data, label)
                    self.assertNotIn(b'board--working', r.data, label)

    def test_health_endpoint_reports_the_deployment_truthfully(self):
        c = create_app().test_client()
        health = json.loads(c.get('/api/research/health').data)
        for field in ('ok', 'database_path', 'database_ephemeral',
                      'serverless', 'providers', 'has_any_ai_key', 'cache'):
            self.assertIn(field, health)
        self.assertIn('entries', health['cache'])
        self.assertIsInstance(health['ok'], bool)

    def test_health_lists_every_registered_provider(self):
        """A provider that is configured but out of credit is the most common
        deployment fault, and the health endpoint must be able to say so."""
        from app.ai.client import PROVIDERS
        health = json.loads(create_app().test_client()
                            .get('/api/research/health').data)
        self.assertEqual([p['name'] for p in health['providers']],
                         [p.name for p in PROVIDERS])
        self.assertIn('groq', [p['name'] for p in health['providers']])
        for entry in health['providers']:
            self.assertIn('has_key', entry)
            self.assertIn('tripped', entry)

    def test_health_never_500s_without_any_keys(self):
        """A health check that fails on a missing optional key is useless."""
        from app.ai.client import PROVIDERS
        saved = {p.key_env: os.environ.pop(p.key_env, None) for p in PROVIDERS}
        try:
            c = create_app().test_client()
            r = c.get('/api/research/health')
            self.assertEqual(r.status_code, 200)
            health = json.loads(r.data)
            self.assertTrue(health['ok'])
            self.assertFalse(health['has_any_ai_key'])
            self.assertFalse(any(p['has_key'] for p in health['providers']))
        finally:
            for k, v in saved.items():
                if v is not None:
                    os.environ[k] = v

    def test_ask_endpoint_still_answers_without_any_keys(self):
        """No key and no reachable search must mean a typed error, never a 500.

        The search step is stubbed to fail outright so the test exercises the
        degradation path deterministically instead of making real calls and
        inheriting whatever a public search engine feels like returning.
        """
        import app.research.agent as am
        from app.research.search import SearchError
        saved_search = am.search

        def boom(*a, **kw):
            raise SearchError("no backend")

        am.search = boom
        saved = os.environ.pop('OPENROUTER_API_KEY', None)
        try:
            c = create_app().test_client()
            r = c.post('/api/research/ask',
                       json={'transaction_type': 'a brand new loan product'})
            self.assertEqual(r.status_code, 503)
            body = json.loads(r.data)
            self.assertIn('error', body)
            self.assertEqual(body['kind'], 'search_unavailable')
            self.assertTrue(body['retryable'])
            # A user-facing message, never an exception repr or a provider name.
            self.assertNotIn('Traceback', body['error'])
            self.assertNotIn('SearchError', body['error'])
            self.assertNotIn('OpenRouter', body['error'])
            self.assertNotIn('HTTP', body['error'])
            self.assertIn('suggestions', body)
            self.assertIsInstance(body['suggestions'], list)
            for suggestion in body['suggestions']:
                self.assertTrue(suggestion['href'].startswith('/checklist?'))
                self.assertTrue(suggestion['label'])
        finally:
            am.search = saved_search
            if saved is not None:
                os.environ['OPENROUTER_API_KEY'] = saved


# ══════════════════════════════════════════════════════════════════════
# Design-system invariants (guards against regressions)
# ══════════════════════════════════════════════════════════════════════
class TestDesignSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        base = os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), 'app', 'static', 'css')
        with open(os.path.join(base, 'main.css')) as fh:
            cls.css = fh.read()

    def test_spacing_scale_is_declared_and_complete(self):
        for step in ('--s1:  8px', '--s2: 16px', '--s3: 24px',
                     '--s4: 32px', '--s5: 48px', '--s6: 64px'):
            self.assertIn(step, self.css)

    def test_gradients_stay_off_the_page_ground(self):
        """Skeuomorphic faces are allowed; a colour wash over the page is not.

        The tactile layer puts a soft vertical gradient on every raised
        surface, which is what makes them read as objects. The page ground is
        different: it carries the paper grain, and a gradient there turns the
        whole page into a wash and kills the grain. So the guard moved from
        "no gradients anywhere" — which the new design legitimately breaks —
        to "no gradient on the ground itself".
        """
        low = self.css.lower()
        for selector in ('body {', 'html {'):
            start = low.find(selector)
            self.assertNotEqual(start, -1, selector)
            block = low[start:low.find('}', start)]
            self.assertNotIn('linear-gradient', block,
                             '%s must stay flat so the paper grain reads' % selector)
        # The old guard also banned a specific washed-out palette. That still
        # holds: these colours never appear in this design.
        for banned in ('#7f5af0', '#8b5cf6', '#6c5ce7', '#a855f7', 'blur(60px)'):
            self.assertNotIn(banned, low)

    def test_five_radii_are_declared_and_the_largest_is_generous(self):
        """Radii grew from three to five when the surfaces went bubbly.

        Still a closed set — an ad-hoc `border-radius: 7px` is exactly how a
        design system quietly stops being one — and still bounded at the top,
        because an unbounded radius is how a card turns into a lozenge.
        """
        import re
        declared = set(re.findall(r'--r-[\w-]+:\s*([\d.]+px|999px)', self.css))
        self.assertEqual(len(declared), 5,
                         "sm/md/lg/xl/pill only: %s" % declared)
        # The pill is 999px by definition and is not a card edge, so it is
        # excluded from the corner-radius bound below.
        sizes = [float(v[:-2]) for v in declared
                 if v.endswith('px') and float(v[:-2]) < 999]
        self.assertGreaterEqual(max(sizes), 24,
                                "the largest radius must stay visibly rounded")
        self.assertLessEqual(max(sizes), 40,
                             "a radius past 40px stops reading as a card edge")

    def test_depth_is_warm_not_neutral_black(self):
        """Inset shadows carry a warm hue; neutral black reads as grey plastic."""
        self.assertIn('--well:', self.css)
        self.assertIn('--shade:', self.css)
        # The inset wells must not be pure black.
        import re
        wells = re.findall(r'--well[\w-]*:\s*([^;]+);', self.css)
        self.assertTrue(wells)
        for value in wells:
            self.assertNotIn('0, 0, 0', value,
                             'inset shadows must be warm: %s' % value)

    def test_every_focusable_control_has_a_visible_focus_style(self):
        self.assertIn(':focus-visible', self.css)
        self.assertIn('.input:focus', self.css)
        self.assertIn('.check:focus-visible', self.css)

    def test_native_appearance_is_reset_on_every_control(self):
        for selector in ('.input, .select', '.check', '.select {'):
            self.assertIn(selector, self.css)
        self.assertIn('appearance: none', self.css)

    def test_reduced_motion_is_respected(self):
        self.assertIn('prefers-reduced-motion', self.css)

    def test_print_styles_exist_and_hide_chrome(self):
        self.assertIn('@media print', self.css)
        for hide in ('.topbar', '.colophon', '.tally', '.no-print'):
            self.assertIn(hide, self.css)

    def test_three_breakpoints_are_covered(self):
        self.assertIn('@media (max-width: 900px)', self.css)
        self.assertIn('@media (max-width: 700px)', self.css)
        self.assertIn('@media (max-width: 600px)', self.css)

    def test_icons_use_a_single_stroke_width_and_are_all_outlined(self):
        base = os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), 'app', 'templates', '_icons.html')
        with open(base) as fh:
            ico = fh.read()
        # Scope to the functional icon set only. The decorative collage macros
        # (wax seal, ink stamp) sit below this point and are deliberately
        # heavier — they are ink and wax, not UI glyphs.
        functional = ico.split('macro wax_seal')[0]
        widths = set(re.findall(r'stroke-width="([\d.]+)"', functional))
        self.assertEqual(widths, {'1.75'},
                         "the icon set must use exactly one stroke width: %s" % widths)
        # Outlined only: the only fill permitted is the svg's own fill="none".
        self.assertNotIn('fill="#', functional)
        self.assertEqual(functional.count('fill="none"'), 1)
        # Every icon is drawn on the same grid with the same joins and caps.
        self.assertEqual(functional.count('viewBox="0 0 24 24"'), 1)
        self.assertIn('stroke-linecap="round"', functional)
        self.assertIn('stroke-linejoin="round"', functional)

    def test_decorative_collage_elements_exist_and_are_not_ui_glyphs(self):
        base = os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), 'app', 'templates', '_icons.html')
        with open(base) as fh:
            ico = fh.read()
        for macro in ('macro wax_seal', 'macro paperclip', 'macro ink_stamp'):
            self.assertIn(macro, ico)
        # All three must be hidden from assistive tech — they carry no meaning.
        self.assertEqual(ico.count('aria-hidden="true"') >= 3, True)

    def test_visual_layers_stay_separate(self):
        """Icon set, characters, and brand mark are three layers, not one.

        The icon set is asserted elsewhere to be fully outlined at a single
        stroke weight, because a regulatory glyph has to be unambiguous at
        16px. The characters and the mark are filled and shaded. Folding any of
        them into _icons.html would break that guarantee, and mixing the three
        styles on one screen is what makes an interface read as assembled
        rather than designed — so the separation is asserted, not just
        documented in a comment.
        """
        tpl = os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), 'app', 'templates')
        with open(os.path.join(tpl, '_icons.html')) as fh:
            ico = fh.read()
        functional = ico.split('macro wax_seal')[0]

        for name in ('_bubble.html', '_logo.html'):
            self.assertTrue(os.path.exists(os.path.join(tpl, name)), name)
        # Neither the characters nor the mark may leak into the icon set.
        self.assertNotIn('bub', functional)
        self.assertNotIn('macro logo_mark', functional)
        # And the icon set must not be referenced for the brand mark.
        base = os.path.join(tpl, 'base.html')
        with open(base) as fh:
            base_html = fh.read()
        self.assertIn('_logo.html', base_html)
        self.assertIn('logo.logo_mark(', base_html)

    def test_favicon_matches_the_brand_mark(self):
        """The tab icon and the masthead mark are the same drawing.

        Two hand-maintained copies of one mark drift apart the moment either is
        edited. This pins the geometry that identifies it: the sheet path, the
        folded corner, the single heavy rule, and the check.
        """
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(root, 'app', 'static', 'favicon.svg')) as fh:
            fav = fh.read()
        with open(os.path.join(root, 'app', 'templates', '_logo.html')) as fh:
            logo = fh.read()

        # The same four primitives, in both files.
        sheet = 'M8 6h10l5 5v15a1 1 0 0 1-1 1H8a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1z'
        fold = 'M18 6l5 5h-5V6z'
        rule = 'M10 15.5h7'
        check = 'M17.6 21.6l2.4 2.4 4.4-4.7'
        for path in (sheet, fold, rule, check):
            self.assertIn(path, fav, path)
            self.assertIn(path, logo, path)
        # One rule, not two — the two-rule version was mush at 30px.
        self.assertEqual(logo.count('M10 15.5h7'), 1)
        self.assertEqual(logo.count('M10 14.5h9'), 0)

    def test_characters_share_one_face_and_one_grid(self):
        """Every bubble character is drawn the same way.

        A cast that drifts — different eyes, different smiles, different
        viewBoxes — reads as five unrelated mascots rather than one family.
        """
        with open(os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), 'app', 'templates', '_bubble.html')) as fh:
            bub = fh.read()
        self.assertEqual(bub.count('viewBox="0 0 200 200"'), 5)
        # The face and the blush are macros, so they are authored once.
        self.assertEqual(bub.count('{% macro _face('), 1)
        self.assertEqual(bub.count('{% macro _blush('), 1)
        # Every character calls the shared face exactly once.
        self.assertEqual(bub.count('{{ _face('), 5)
        self.assertEqual(bub.count('{{ _blush('), 5)
        # Filled shapes, like the brand mark — the opposite of the icon set.
        self.assertIn('fill-opacity="0.30"', bub)


if __name__ == '__main__':
    unittest.main(verbosity=2)


# ══════════════════════════════════════════════════════════════════════
# The research job lifecycle, over HTTP
#
# This is the exact code path a live demo runs: POST /start, then poll
# /status until done, then the browser re-requests the page. It could not be
# exercised against a real provider mid-session (API credit), so it is
# exercised here against a stubbed one — the threading, the polling contract,
# the progress payload the flip-board reads, and the browser's follow-up
# request are all real.
# ══════════════════════════════════════════════════════════════════════
class TestJobLifecycleOverHTTP(unittest.TestCase):

    def setUp(self):
        import app.research.agent as agent_mod
        self.app = create_app()
        self.tmp = tempfile.mkdtemp()
        self.app.config['DATABASE'] = os.path.join(self.tmp, 't.db')
        cache_mod.init_schema(self.app)
        self.c = self.app.test_client()
        self._agent = agent_mod


    def tearDown(self):
        import app.research.agent as am
        if getattr(self, '_orig_search', None) is not None:
            am.search = self._orig_search
        if getattr(self, '_orig_synth', None) is not None:
            am.synthesize = self._orig_synth

    def test_start_poll_done_then_page_renders(self):
        import app.research.agent as am
        self._orig_search, self._orig_synth = am.search, am.synthesize
        am.search = lambda *a, **kw: {
            "findings": "stub findings",
            "citations": [{"url": "https://bank.example/doc", "title": "Doc"},
                          {"url": "https://rbi.example/circ", "title": "RBI"}],
            "model": "stub-model", "provider": "openrouter:web",
            "latency_ms": 5, "query": "q", "searched_at": "2026-09-27T00:00:00",
        }
        am.synthesize = lambda *a, **kw: {"answer": {
            "summary": "stub summary",
            "items": [{"step_order": 1, "document_name": "PAN card",
                       "plain_explanation": "e", "where_to_obtain": "w",
                       "approx_cost_min": 0, "approx_cost_max": 0,
                       "approx_time_days": 1, "regulatory_source": "rbi",
                       "depends_on": "", "source_note": "s"}],
            # The real normaliser copies every citation onto the answer, so
            # the stub does too — otherwise the test would be asserting a
            # shape the pipeline never produces.
            "sources": [{"url": "https://bank.example/doc", "title": "Doc"},
                        {"url": "https://rbi.example/circ", "title": "RBI"}]},
            "provider": "openrouter", "model": "", "raw": ""}

        # 1. The browser asks for a cold question -> researching view
        page = self.c.get('/checklist?transaction_type=stub+loan+for+testing'
                          '&bank=Stub+Bank&residency=resident')
        self.assertIn(b'board--working', page.data)

        # 2. It starts a job
        started = self.c.post('/api/research/start', json={
            'transaction_type': 'stub loan for testing', 'bank': 'Stub Bank',
            'residency': 'resident',
        })
        self.assertEqual(started.status_code, 202)
        job_id = json.loads(started.data)['job_id']
        self.assertTrue(job_id)

        # 3. It polls until done. The contract the flip-board depends on is
        #    that every intermediate payload carries `stages` and `citations`.
        import time
        payload, polls = None, 0
        deadline = time.time() + 20
        while time.time() < deadline:
            polls += 1
            r = self.c.get('/api/research/status/' + job_id)
            self.assertEqual(r.status_code, 200)
            payload = json.loads(r.data)
            if payload['status'] in ('done', 'error'):
                break
            time.sleep(0.2)
        self.assertIsNotNone(payload)
        self.assertEqual(payload['status'], 'done',
                         "job did not complete: %s" % payload)
        self.assertGreaterEqual(polls, 1)
        self.assertIn('elapsed', payload)
        self.assertIn('stages', payload)
        self.assertIn('citations', payload)

        result = payload['result']
        self.assertEqual(result['cache'], 'miss')
        self.assertEqual(result['total'], 1)
        self.assertEqual(len(result['sources']), 2)
        self.assertEqual(result['request']['bank'], 'Stub Bank')

        # 4. The browser re-requests the page, which must now hit the cache
        page2 = self.c.get('/checklist?transaction_type=stub+loan+for+testing'
                           '&bank=Stub+Bank&residency=resident&just=1')
        self.assertEqual(page2.status_code, 200)
        self.assertIn(b'PAN card', page2.data)
        self.assertIn(b'Sources read for this answer', page2.data)
        self.assertNotIn(b'board--working', page2.data)

    def test_job_error_is_typed_and_the_page_still_renders(self):
        import app.research.agent as am
        from app.research.search import SearchError
        self._orig_search, self._orig_synth = am.search, am.synthesize

        def boom(*a, **kw):
            raise SearchError("stubbed outage")

        am.search = boom
        am.synthesize = lambda *a, **kw: {"answer": None, "provider": "x",
                                          "model": "", "raw": ""}

        page = self.c.get('/checklist?transaction_type=another+stub+loan')
        self.assertIn(b'board--working', page.data)

        job_id = json.loads(self.c.post('/api/research/start', json={
            'transaction_type': 'another stub loan'}).data)['job_id']

        import time
        payload, deadline = None, time.time() + 20
        while time.time() < deadline:
            payload = json.loads(self.c.get('/api/research/status/' + job_id).data)
            if payload['status'] in ('done', 'error'):
                break
            time.sleep(0.2)
        self.assertEqual(payload['status'], 'error')
        self.assertIn('message', payload['error'])
        self.assertIn('kind', payload['error'])
        self.assertNotIn('Traceback', payload['error']['message'])
        self.assertNotIn('SearchError', payload['error']['message'])

    def test_start_rejects_a_blank_transaction_before_spawning_a_thread(self):
        r = self.c.post('/api/research/start', json={'transaction_type': '   '})
        self.assertEqual(r.status_code, 400)
        body = json.loads(r.data)
        self.assertEqual(body['kind'], 'invalid_request')
        self.assertFalse(body['retryable'])


# ══════════════════════════════════════════════════════════════════════
# Direct search backend
#
# The keyless search path is pure parsing and ranking, so every branch is
# testable without a network call. These tests exist because the bugs found
# here were all silent: a percent-encoding mistake produced URLs that looked
# plausible and simply never fetched, and an HTTP 202 anti-bot page parsed as
# "zero results" and surfaced as a misleading "no search backend available".
# ══════════════════════════════════════════════════════════════════════
class TestDirectSearch(unittest.TestCase):

    def test_percent_encoded_result_urls_are_decoded(self):
        """DuckDuckGo wraps URLs in a percent-encoded uddg parameter.

        html.unescape alone leaves https%3A%2F%2F... which looks like a URL
        to a regex and 404s to a server. This is the bug that made an early
        version fetch 0 of 5 pages while reporting no error.
        """
        from app.research.search import _decode_url
        raw = "https%3A%2F%2Fhomeloans.sbi.bank.in%2Fproducts%2Fview%2Fnri-home-loan"
        self.assertEqual(_decode_url(raw),
                         "https://homeloans.sbi.bank.in/products/view/nri-home-loan")

    def test_parse_ddg_lite_extracts_titles_and_urls(self):
        from app.research.search import _parse_ddg_lite
        from urllib.parse import quote
        target = "https://homeloans.sbi.bank.in/products/view/nri-home-loan"
        html = (
            '<a rel="nofollow" href="//duckduckgo.com/l/?uddg=%s">'
            '<strong>NRI</strong> Home Loan Documents</a>' % quote(target, safe="")
        )
        hits = _parse_ddg_lite(html)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]['url'], target)
        self.assertIn('Home Loan', hits[0]['title'])

    def test_parse_ddg_html_extracts_titles_and_urls(self):
        from app.research.search import _parse_ddg_html
        from urllib.parse import quote
        target = "https://www.urbanmoney.com/home-loan/sbi"
        html = ('<a rel="nofollow" class="result__a" '
                'href="//duckduckgo.com/l/?uddg=%s">Documents Required</a>'
                % quote(target, safe=""))
        hits = _parse_ddg_html(html)
        self.assertEqual(hits[0]['url'], target)
        self.assertEqual(hits[0]['title'], 'Documents Required')

    def test_duplicate_results_are_collapsed(self):
        from app.research.search import _parse_ddg_lite
        from urllib.parse import quote
        target = "https://example.com/a"
        row = ('<a href="//duckduckgo.com/l/?uddg=%s">Title</a>' % quote(target, safe=""))
        self.assertEqual(len(_parse_ddg_lite(row * 4)), 1)

    def test_anti_bot_responses_are_detected(self):
        """HTTP 202 with a challenge body is a throttle, not a success."""
        from app.research.search import _looks_blocked

        class R:
            def __init__(self, code):
                self.status_code = code

        for code in (202, 429, 503):
            self.assertTrue(_looks_blocked(R(code), "<html>ok</html>"), code)
        self.assertFalse(_looks_blocked(R(200), "<html>results</html>"))
        for marker in ('anomaly', 'captcha', 'unusual traffic', 'are you a robot'):
            self.assertTrue(_looks_blocked(R(200), marker), marker)

    def test_junk_hosts_are_excluded(self):
        from app.research.search import _SKIP_HOSTS
        for host in ('scribd.com', 'slideshare.net', 'reddit.com', 'youtube.com'):
            self.assertIn(host, _SKIP_HOSTS)

    def test_bank_official_page_outranks_a_listicle(self):
        """This ranking is the difference between a sourced answer and SEO
        sludge: a bank publishing about itself beats any third-party summary."""
        from app.research.search import _tier, _rank
        official = {"url": "https://homeloans.sbi.bank.in/products/view/nri-home-loan",
                    "title": "SBI NRI Home Loan"}
        listicle = {"url": "https://www.someblog.com/best-sbi-home-loan-docs",
                    "title": "Best SBI home loan documents 2026"}
        regulator = {"url": "https://www.rbi.org.in/circular", "title": "RBI"}

        self.assertLess(_tier(official, "State Bank of India"), _tier(listicle,
                                                                   "State Bank of India"))
        self.assertLess(_tier(regulator, ""), _tier(listicle, ""))

        ranked = _rank([listicle, official, regulator], "State Bank of India")
        urls = [r['url'] for r in ranked]
        # RBI first, then the bank's own page, then the listicle last.
        self.assertEqual(urls[0], regulator['url'])
        self.assertLess(urls.index(official['url']), urls.index(listicle['url']))

    def test_ranking_is_stable_within_a_tier(self):
        """Sorting must not flatten DuckDuckGo's relevance order into
        alphabetical order — that would lose its ranking entirely."""
        from app.research.search import _rank
        a = {"url": "https://zebra.com/1", "title": "z"}
        b = {"url": "https://apple.com/2", "title": "a"}
        ranked = _rank([a, b], "")
        self.assertEqual([r['url'] for r in ranked], [a['url'], b['url']])

    def test_unknown_bank_still_gets_tiered_not_rejected(self):
        from app.research.search import _tier
        hit = {"url": "https://karnatakabank.example/loans", "title": "x"}
        self.assertEqual(_tier(hit, "Karnataka Bank"), 0)

    def test_strip_html_removes_scripts_and_tags(self):
        from app.research.search import _strip_html
        raw = ('<html><head><style>b{}</style></head><body>'
               '<script>evil()</script><h1>Title</h1><p>Body &amp; more</p>'
               '<!-- comment --></body></html>')
        out = _strip_html(raw)
        self.assertIn('Title', out)
        self.assertIn('Body & more', out)
        for junk in ('evil()', '<script', 'b{}', 'comment'):
            self.assertNotIn(junk, out)

    def test_page_fetch_returns_none_for_dead_links_not_raising(self):
        from app.research.search import _fetch_page
        # Reserved TLD, guaranteed not to resolve.
        self.assertIsNone(_fetch_page({"url": "http://nope.invalid/x", "title": "t"}))

    def test_direct_search_throttle_uses_the_bounded_retry_then_falls_through(self):
        """A blocked direct search must reach the configured retry path."""
        import app.research.search as sm
        from app.research.search import _RateLimited, SearchError

        calls = []

        def blocked(*a, **kw):
            calls.append(1)
            raise _RateLimited("blocked")

        original_results, original_retries, original_models = (
            sm._results_for, sm.DIRECT_SEARCH_RETRIES, sm.SEARCH_MODELS)
        sm._results_for = blocked
        sm.DIRECT_SEARCH_RETRIES = (0, 0)
        sm.SEARCH_MODELS = []
        try:
            with self.assertRaises(SearchError) as ctx:
                sm.search('home loan', bank='X Bank',
                          residency_phrase='an applicant', state='')
            self.assertIn('throttled', str(ctx.exception))
        finally:
            sm._results_for = original_results
            sm.DIRECT_SEARCH_RETRIES = original_retries
            sm.SEARCH_MODELS = original_models
        self.assertEqual(len(calls), len((0, 0)))

    def test_search_falls_through_when_direct_is_throttled(self):
        """A throttle must not abort the pipeline — there is a second backend.

        With the direct path throttled and every model-native fallback failing,
        the caller still gets a typed SearchError, but the message must say
        that throttling happened. An error that reads "no backend available"
        when the truth is "we were rate-limited" sends the reader looking in
        entirely the wrong place.
        """
        import app.research.search as sm
        from app.research.search import _RateLimited, SearchError

        def throttled(*a, **kw):
            raise _RateLimited("blocked")

        # Cut the retry sleeps and the model fallbacks out of the test.
        original_search, original_retries, original_models = (
            sm._direct_search, sm.DIRECT_SEARCH_RETRIES, sm.SEARCH_MODELS)
        original_call = sm._call_openrouter_search
        sm._direct_search = throttled
        sm.DIRECT_SEARCH_RETRIES = (0,)
        sm.SEARCH_MODELS = []
        try:
            with self.assertRaises(SearchError) as ctx:
                sm.search('home loan', bank='X Bank',
                          residency_phrase='an applicant', state='')
            self.assertIn('throttled', str(ctx.exception))
        finally:
            sm._direct_search = original_search
            sm.DIRECT_SEARCH_RETRIES = original_retries
            sm.SEARCH_MODELS = original_models
            sm._call_openrouter_search = original_call

    def test_search_returns_direct_results_without_touching_openrouter(self):
        """The direct path must be self-sufficient: no paid key, no OpenRouter."""
        import app.research.search as sm

        def fake_direct(*a, **kw):
            return {"findings": "page text", "citations": [
                        {"url": "https://bank.example/doc", "title": "Doc"}],
                    "model": "duckduckgo + direct-fetch", "provider": "direct",
                    "latency_ms": 900, "searched_at": "2026-09-27T00:00:00"}

        def explode(*a, **kw):
            raise AssertionError("must not call OpenRouter on the direct path")

        original_direct, original_call = sm._direct_search, sm._call_openrouter_search
        sm._direct_search = fake_direct
        sm._call_openrouter_search = explode
        try:
            out = sm.search('home loan', bank='X Bank',
                            residency_phrase='an applicant', state='')
        finally:
            sm._direct_search = original_direct
            sm._call_openrouter_search = original_call

        self.assertEqual(out['provider'], 'direct')
        self.assertEqual(out['model'], 'duckduckgo + direct-fetch')
        self.assertEqual(len(out['citations']), 1)
        self.assertIn('query', out)

    def test_retry_schedule_is_bounded(self):
        from app.research.search import DIRECT_SEARCH_RETRIES
        self.assertTrue(DIRECT_SEARCH_RETRIES[0] == 0)
        self.assertEqual(list(DIRECT_SEARCH_RETRIES),
                         sorted(DIRECT_SEARCH_RETRIES), "must grow")
        self.assertLess(sum(DIRECT_SEARCH_RETRIES), 60,
                        "total backoff must not exceed a cold-research wait")


# ══════════════════════════════════════════════════════════════════════
# Provider registry
#
# Three behaviours here are load-bearing and all were found the hard way:
# skipping providers with no key, tripping out providers that are out of
# credit, and discovering Groq's model list instead of hardcoding it.
# ══════════════════════════════════════════════════════════════════════
def _http_error(status):
    """A requests.HTTPError that actually carries its status code.

    The circuit breaker reads `exc.response.status_code`, exactly as it does
    with a live response, so a test double has to set the same attribute or it
    is not testing the same contract.
    """
    import requests
    response = requests.Response()
    response.status_code = status
    err = requests.HTTPError("%d error" % status, response=response)
    return err


class TestProviderRegistry(unittest.TestCase):

    def setUp(self):
        from app.ai import client
        self.client = client
        self.saved_env = {p.key_env: os.environ.get(p.key_env)
                          for p in client.PROVIDERS}
        self.saved_trip = dict(client._tripped)
        client._tripped.clear()
        self.addCleanup(self._restore)

    def _restore(self):
        c = self.client
        c._tripped.clear()
        c._tripped.update(self.saved_trip)
        for env, value in self.saved_env.items():
            if value is None:
                os.environ.pop(env, None)
            else:
                os.environ[env] = value
        c._reset_groq_cache()

    def _clear_keys(self):
        for p in self.client.PROVIDERS:
            os.environ.pop(p.key_env, None)

    # ── registry shape ────────────────────────────────────────────────
    def test_groq_is_registered_between_openrouter_and_nim(self):
        names = [p.name for p in self.client.PROVIDERS]
        self.assertEqual(names, ['openrouter', 'groq', 'nvidia_nim'])
        self.assertEqual(self.client.GROQ.key_env, 'GROQ_API_KEY')

    def test_groq_uses_the_openai_compatible_endpoint(self):
        self.assertIn('api.groq.com/openai/v1/chat/completions',
                      self.client.GROQ.url)

    def test_every_provider_declares_at_least_one_model(self):
        for p in self.client.PROVIDERS:
            self.assertTrue(p.models, p.name)

    # ── skipping and tripping ─────────────────────────────────────────
    def test_provider_with_no_key_is_skipped_without_being_called(self):
        """An unauthenticated call is a wasted round trip on every request."""
        self._clear_keys()
        calls = []

        def explode(*a, **kw):
            calls.append(1)
            raise AssertionError("must not call a provider with no key")

        original = self.client.call_provider
        self.client.call_provider = explode
        try:
            with self.assertRaises(Exception):
                self.client.call_chain("s", "u", 100)
        finally:
            self.client.call_provider = original
        self.assertEqual(calls, [])

    def test_no_keys_at_all_raises_rather_than_inventing_an_answer(self):
        self._clear_keys()
        with self.assertRaises(ValueError):
            self.client.call_chain("sys", "user", 100)

    def test_out_of_credit_provider_is_tripped_and_skipped_afterwards(self):
        """The OpenRouter key here is a free tier with no credit. Without a
        breaker, every generation opens with a guaranteed ~200ms 402."""
        os.environ[self.client.OPENROUTER.key_env] = "dead-key"
        os.environ[self.client.GROQ.key_env] = "good-key"
        calls = []

        def fake_post(provider, model, *a, **kw):
            calls.append(provider.name)
            if provider.name == "openrouter":
                raise _http_error(402)
            return "{}", "fake-model"

        original = self.client._post
        self.client._post = fake_post
        try:
            text, provider_name, _ = self.client.call_chain("sys", "user", 100)
            self.assertEqual(provider_name, "groq")
            self.assertEqual(calls, ["openrouter", "groq"], "no repeated 402s")

            # Second call must go straight to Groq.
            calls.clear()
            self.client.call_chain("sys", "user", 100)
        finally:
            self.client._post = original

        self.assertEqual(calls, ["groq"],
                         "tripped provider should not be retried this process")

    def test_a_model_404_does_not_retry_other_slugs_on_the_same_provider(self):
        """A retired slug on one provider says nothing about its other models
        once the provider itself has said it cannot serve."""
        os.environ[self.client.GROQ.key_env] = "k"
        seen = []

        def fake_post(provider, model, *a, **kw):
            seen.append(model)
            raise _http_error(404)

        original = self.client._post
        self.client._post = fake_post
        try:
            with self.assertRaises(Exception):
                self.client.call_provider(self.client.GROQ, "s", "u", 10)
        finally:
            self.client._post = original
        self.assertEqual(len(seen), 1, "must not walk the whole model list")
        self.assertTrue(self.client._is_tripped(self.client.GROQ))

    def test_trip_expires_so_a_topped_up_key_recovers(self):
        p = self.client.GROQ
        self.client._trip(p, "HTTP 402")
        self.assertTrue(self.client._is_tripped(p))
        self.client._tripped[p.name] = ("HTTP 402", 0.0)  # ancient
        self.assertFalse(self.client._is_tripped(p),
                         "a tripped provider must be retried after the grace "
                         "period, since a key can be topped up mid-session")

    def test_a_working_provider_is_not_left_tripped(self):
        p = self.client.GROQ
        os.environ[p.key_env] = "k"
        self.client._trip(p, "HTTP 402")
        self.client._reset_trip(p)
        self.assertFalse(self.client._is_tripped(p))

    def test_transient_status_is_not_tripped(self):
        """A 500 or a bad request is a fault of that one call, not a reason to
        abandon a provider for five minutes. Only auth/quota/gone are terminal."""
        os.environ[self.client.GROQ.key_env] = "k"
        for status in (500, 400, 422, 503):
            with self.subTest(status=status):
                self.client._tripped.clear()

                def fake_post(provider, model, *a, **kw):
                    raise _http_error(status)

                original = self.client._post
                self.client._post = fake_post
                try:
                    with self.assertRaises(Exception):
                        self.client.call_provider(self.client.GROQ, "s", "u", 10)
                finally:
                    self.client._post = original
                self.assertFalse(self.client._is_tripped(self.client.GROQ),
                                 "%d should not trip the provider" % status)

    def test_terminal_statuses_are_the_ones_we_trip_on(self):
        self.assertEqual(set(self.client._DEAD_STATUSES),
                         {401, 402, 403, 404, 410, 429})

    def test_health_lists_providers_with_key_and_trip_state(self):
        os.environ[self.client.GROQ.key_env] = "k"
        self._clear_keys()
        os.environ[self.client.GROQ.key_env] = "k"
        health = {p['name']: p for p in self.client.provider_health()}
        self.assertTrue(health['groq']['has_key'])
        self.assertFalse(health['openrouter']['has_key'])
        self.assertIn('tripped', health['groq'])

    # ── Groq model discovery ──────────────────────────────────────────
    def test_groq_models_are_discovered_not_hardcoded(self):
        """The account in use does not serve llama-3.3-70b-versatile at all —
        a hardcoded list would 404. Verified against /models."""
        class FakeModels:
            @staticmethod
            def get(url, headers=None, timeout=None):
                self.assertIn("api.groq.com", url)
                self.assertIn("Authorization", headers)

                class R:
                    status_code = 200

                    @staticmethod
                    def json():
                        return {"data": [{"id": "openai/gpt-oss-120b"},
                                         {"id": "qwen/qwen3.8-27b"},
                                         {"id": "whisper-large-v3"},
                                         {"id": "openai/gpt-oss-safeguard-20b"},
                                         {"id": "meta-llama/llama-prompt-guard-2-22m"},
                                         {"id": "canopylabs/orpheus-arabic-saudi"}]}
                return R()

        import requests
        self.assertIn(self.client.GROQ.key_env, self.saved_env)
        os.environ[self.client.GROQ.key_env] = "k"
        original = requests.get
        requests.get = FakeModels.get
        try:
            self.client._reset_groq_cache()
            models = self.client._fetch_groq_models()
        finally:
            requests.get = original
            self.client._reset_groq_cache()

        self.assertEqual(models[0], "openai/gpt-oss-120b")
        self.assertIn("qwen/qwen3.8-27b", models)
        for junk in ("whisper-large-v3", "safeguard", "prompt-guard", "orpheus"):
            self.assertNotIn(junk, str(models))

    def test_groq_fallbacks_survive_when_preferred_models_are_absent(self):
        """`ordered or rest` silently dropped the fallback list; this asserts
        preferred and discovered models are concatenated."""
        class FakeModels:
            @staticmethod
            def get(url, headers=None, timeout=None):
                class R:
                    status_code = 200

                    @staticmethod
                    def json():
                        return {"data": [{"id": "qwen/qwen3.8-27b"},
                                         {"id": "openai/gpt-oss-120b"},
                                         {"id": "openai/gpt-oss-20b"}]}
                return R()

        import requests
        os.environ[self.client.GROQ.key_env] = "k"
        original = requests.get
        requests.get = FakeModels.get
        try:
            self.client._reset_groq_cache()
            models = self.client._fetch_groq_models()
        finally:
            requests.get = original
            self.client._reset_groq_cache()

        self.assertEqual(len(models), 3,
                         "every usable model must survive, not just the "
                         "preferred slice: %s" % models)
        self.assertEqual(models[0], "openai/gpt-oss-120b")

    def test_groq_falls_back_to_the_static_shortlist_when_discovery_fails(self):
        import requests
        os.environ[self.client.GROQ.key_env] = "k"

        def boom(*a, **kw):
            raise requests.ConnectionError("network down")

        original = requests.get
        requests.get = boom
        try:
            self.client._reset_groq_cache()
            models = self.client._fetch_groq_models()
        finally:
            requests.get = original
            self.client._reset_groq_cache()
        self.assertTrue(models, "must never leave Groq with no models")

    def test_groq_without_a_key_uses_the_static_shortlist(self):
        self._clear_keys()
        self.client._reset_groq_cache()
        self.assertEqual(self.client._fetch_groq_models(),
                         list(self.client.GROQ.models))

    # ── JSON handling across providers ─────────────────────────────────
    def test_json_mode_is_omitted_for_providers_that_ignore_it(self):
        sent = {}

        def fake_post(provider, model, *a, **kw):
            sent['json_mode'] = kw.get('json_mode')
            sent['supports'] = provider.supports_json
            return "{}", "m"

        nim = self.client.NIM
        self.assertTrue(nim.supports_json,
                        "NIM honours response_format on the verified models")
