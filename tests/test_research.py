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
                      'serverless', 'has_openrouter_key', 'cache'):
            self.assertIn(field, health)
        self.assertIn('entries', health['cache'])
        self.assertIsInstance(health['ok'], bool)

    def test_health_never_500s_without_any_keys(self):
        """A health check that fails on a missing optional key is useless."""
        import app as app_pkg
        saved = {k: os.environ.pop(k, None)
                 for k in ('OPENROUTER_API_KEY', 'NVIDIA_NIM_API_KEY')}
        try:
            application = create_app()
            c = application.test_client()
            r = c.get('/api/research/health')
            self.assertEqual(r.status_code, 200)
            health = json.loads(r.data)
            self.assertFalse(health['has_openrouter_key'])
            self.assertTrue(health['ok'])
        finally:
            for k, v in saved.items():
                if v is not None:
                    os.environ[k] = v

    def test_ask_endpoint_still_answers_without_any_keys(self):
        """No key must mean a graceful typed error, never a 500."""
        import app as app_pkg
        saved = os.environ.pop('OPENROUTER_API_KEY', None)
        try:
            app = create_app()
            c = app.test_client()
            r = c.post('/api/research/ask',
                       json={'transaction_type': 'a brand new loan product'})
            self.assertIn(r.status_code, (200, 503))
            body = json.loads(r.data)
            if r.status_code == 503:
                self.assertIn('error', body)
                self.assertNotIn('Traceback', body['error'])
                self.assertNotIn('OpenRouter', body['error'])
        finally:
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

    def test_no_legacy_gradient_decoration(self):
        low = self.css.lower()
        # One linear-gradient remains, used to rule the board like a ledger
        # card. It is a repeating 1px rule, not a colour wash.
        gradient_uses = low.count('linear-gradient')
        self.assertLessEqual(gradient_uses, 1)
        for banned in ('#7f5af0', '#8b5cf6', '#6c5ce7', '#a855f7',
                       'radial-gradient(circle at 30% 30%', 'blur(60px)'):
            self.assertNotIn(banned, low)

    def test_three_radii_only(self):
        import re
        declared = set(re.findall(r'--r-[\w-]+:\s*([\d.]+px|999px)', self.css))
        self.assertEqual(len(declared), 4, "sm/md/lg/pill only: %s" % declared)

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
        for hide in ('.masthead', '.colophon', '.tally', '.no-print'):
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
