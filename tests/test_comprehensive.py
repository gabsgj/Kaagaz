"""
Comprehensive tests for Kaagaz.
Covers: all routes, all transaction types × states, data integrity,
AI provider fallback chain, regulatory source correctness, template rendering.
"""
import json
import os
import sys
import sqlite3
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app import create_app


# ──────────────────────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def app():
    application = create_app()
    application.config['TESTING'] = True
    return application

@pytest.fixture(scope="module")
def client(app):
    with app.test_client() as c:
        yield c

@pytest.fixture(scope="module")
def db(app):
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


# ──────────────────────────────────────────────────────────────
# 1. Homepage
# ──────────────────────────────────────────────────────────────

# The four regulatory buckets. The RBI / state split is the correctness rule
# this whole product exists to get right, so it is asserted in several places.
VALID_REGULATORY_SOURCES = {'rbi', 'state_stamp_act', 'registrar', 'bank_internal'}


# ══════════════════════════════════════════════════════════════════════
# 1. Ask page  (Phase 2: free-text question, not a four-item menu)
# ══════════════════════════════════════════════════════════════════════

class TestAskPage:
    def test_returns_200(self, client):
        assert client.get('/').status_code == 200

    def test_contains_branding(self, client):
        html = client.get('/').data.decode()
        assert 'Kaagaz' in html
        assert 'wordmark__text' in html

    def test_is_a_free_text_question_not_a_fixed_menu(self, client):
        """Phase 2 removed the four-category ceiling; the input must be free text."""
        html = client.get('/').data.decode()
        assert 'name="transaction_type"' in html
        assert 'list="category-list"' in html          # a datalist suggests, never restricts
        assert 'name="bank"' in html and 'list="bank-list"' in html
        assert 'name="state"' in html and 'list="state-list"' in html
        # The old two-state radio pair must be gone.
        assert 'data-tx="home_loan"' not in html
        assert 'data-state="kerala"' not in html

    def test_offers_every_residency_state(self, client):
        html = client.get('/').data.decode()
        for label in ('Resident Indian', 'Non-Resident Indian (NRI)',
                      'Mixed', 'All-NRI', 'Not applicable'):
            assert label in html, label

    def test_contains_ledger_strip(self, client):
        html = client.get('/').data.decode()
        assert 'class="ledger"' in html
        assert 'Describe the transaction' in html

    def test_states_cache_is_a_floor_not_a_ceiling(self, client):
        """The copy must not imply the pre-seeded entries are the limit."""
        html = client.get('/').data.decode()
        assert 'The cache is a floor, not a ceiling' in html

    def test_no_placeholder_text(self, client):
        html = client.get('/').data.decode().lower()
        for junk in ('lorem ipsum', 'dolor sit', 'tbd', 'todo', 'coming soon'):
            assert junk not in html, junk

    def test_disclaimer_present(self, client):
        assert 'not legal or financial advice' in client.get('/').data.decode()


# ══════════════════════════════════════════════════════════════════════
# 2. Result page
# ══════════════════════════════════════════════════════════════════════

# (transaction, bank, residency) triples that are guaranteed pre-warmed.
RESULT_CASES = [
    ('home loan', 'HDFC Bank', 'resident'),
    ('home loan', 'State Bank of India', 'nri'),
    ('gold loan', 'State Bank of India', 'resident'),
    ('mudra loan', '', 'resident'),
]


def _get(client, tx, bank='', residency='resident', state=''):
    parts = ['transaction_type=' + tx.replace(' ', '+')]
    if bank:
        parts.append('bank=' + bank.replace(' ', '+'))
    if state:
        parts.append('state=' + state.replace(' ', '+'))
    parts.append('residency=' + residency)
    return client.get('/checklist?' + '&'.join(parts)).data.decode()


# A pre-warmed case used by the per-feature structural assertions below.
GOLD_SBI = ('/checklist?transaction_type=gold+loan'
            '&bank=State+Bank+of+India&residency=resident')


def _gold_sbi(client):
    return client.get(GOLD_SBI).data.decode()


class TestResultPage:
    def test_returns_200(self, client):
        for tx, bank, res in RESULT_CASES:
            r = client.get('/checklist?transaction_type=%s&bank=%s&residency=%s'
                           % (tx.replace(' ', '+'), bank.replace(' ', '+'), res))
            assert r.status_code == 200, (tx, bank, res)

    def test_contains_steps(self, client):
        for tx, bank, res in RESULT_CASES:
            html = client.get('/checklist?transaction_type=%s&bank=%s&residency=%s'
                              % (tx.replace(' ', '+'), bank.replace(' ', '+'),
                                 res)).data.decode()
            assert 'class="step"' in html, tx
            assert 'step__why' in html, tx
            assert 'step__facts' in html, tx

    def test_contains_progress_board(self, client):
        html = _gold_sbi(client)
        assert 'class="board"' in html
        assert 'Documents ready' in html

    def test_contains_flip_number_cells(self, client):
        """Phase 2 renders fixed-width digit cells, not a bare <span>."""
        html = _gold_sbi(client)
        assert 'id="doneCount"' in html
        assert 'id="totalCount"' in html
        assert 'class="flip"' in html
        assert 'data-min=' in html        # minimum digit width, the anti-jitter hook

    def test_contains_explain_button(self, client):
        html = _gold_sbi(client)
        assert 'step__explain' in html
        assert 'Why is this needed?' in html

    def test_contains_sticky_tally(self, client):
        html = _gold_sbi(client)
        assert 'class="tally"' in html
        assert 'tally__fill' in html

    def test_contains_provenance_and_sources(self, client):
        html = _gold_sbi(client)
        assert 'Researched' in html
        assert 'Sources read for this answer' in html
        assert 'https://' in html

    def test_contains_legend(self, client):
        html = _gold_sbi(client)
        assert 'RBI rules' in html
        assert 'State stamp act' in html

    def test_contains_step_numbers(self, client):
        html = _gold_sbi(client)
        assert 'step__num' in html
        assert '>01<' in html

    def test_contains_status_badges(self, client):
        html = _gold_sbi(client)
        assert 'class="status"' in html
        assert 'data-state="pending"' in html

    def test_contains_dependency_notices(self, client):
        html = client.get('/checklist?transaction_type=home+loan&bank=HDFC+Bank'
                          '&residency=resident').data.decode()
        assert 'step__depends' in html

    def test_contains_regulatory_attribution_per_item(self, client):
        html = _gold_sbi(client)
        assert 'step__gov-mark' in html
        assert 'data-source=' in html

    def test_shows_bank_and_state_badges_when_given(self, client):
        html = client.get('/checklist?transaction_type=property+registration'
                          '&state=Kerala').data.decode()
        assert 'Kerala' in html

    def test_back_link_present(self, client):
        html = client.get('/checklist?transaction_type=gold+loan').data.decode()
        assert 'Ask a different question' in html

    def test_no_placeholder_text(self, client):
        html = _gold_sbi(client).lower()
        for junk in ('lorem ipsum', 'dolor sit', 'tbd', 'todo', 'coming soon'):
            assert junk not in html, junk

    def test_invalid_request_is_handled_with_a_real_message(self, client):
        r = client.get('/checklist?transaction_type=&bank=x')
        assert r.status_code == 400
        assert 'Tell us what you' in r.data.decode()

    def test_uncached_question_gets_the_researching_view(self, client):
        html = client.get('/checklist?transaction_type=zzzz+novel+thing'
                          '&bank=Nowhere+Bank').data.decode()
        assert 'board--working' in html
        assert 'Not in the cache' in html


class TestDataIntegrity:
    def test_total_row_count_sufficient(self, db):
        count = db.execute('SELECT COUNT(*) FROM checklist_items').fetchone()[0]
        assert count >= 50, f"Only {count} rows — expected at least 50"

    def test_all_four_transaction_types_present(self, db):
        types = {r[0] for r in db.execute('SELECT DISTINCT transaction_type FROM checklist_items')}
        assert types == {'home_loan', 'nri_account', 'property_registration', 'business_account'}

    def test_both_states_present_for_state_dependent_types(self, db):
        for tx in ['home_loan', 'property_registration', 'business_account']:
            states = {r[0] for r in db.execute(
                'SELECT DISTINCT state FROM checklist_items WHERE transaction_type=? AND state IS NOT NULL', (tx,)
            )}
            assert 'kerala' in states, f"No Kerala rows for {tx}"
            assert 'maharashtra' in states, f"No Maharashtra rows for {tx}"

    def test_nri_account_has_no_state_rows(self, db):
        count = db.execute(
            "SELECT COUNT(*) FROM checklist_items WHERE transaction_type='nri_account' AND state IS NOT NULL"
        ).fetchone()[0]
        assert count == 0, "NRI account should have no state-specific rows"

    def test_regulatory_source_values_are_valid_enum(self, db):
        rows = db.execute('SELECT id, document_name, regulatory_source FROM checklist_items').fetchall()
        for row in rows:
            assert row['regulatory_source'] in VALID_REGULATORY_SOURCES, \
                f"Invalid regulatory_source '{row['regulatory_source']}' on row {row['id']} ({row['document_name']})"

    def test_stamp_duty_never_attributed_to_rbi(self, db):
        """State stamp duty must NEVER have regulatory_source=rbi."""
        rows = db.execute(
            """SELECT document_name, regulatory_source FROM checklist_items
               WHERE lower(document_name) LIKE '%stamp duty%'
                  OR lower(document_name) LIKE '%franking%'
                  OR lower(document_name) LIKE '%adhesive stamp%'"""
        ).fetchall()
        for row in rows:
            assert row['regulatory_source'] != 'rbi', \
                f"'{row['document_name']}' has regulatory_source=rbi — stamp duty is a state subject"

    def test_registration_fees_never_attributed_to_rbi(self, db):
        rows = db.execute(
            """SELECT document_name, regulatory_source FROM checklist_items
               WHERE lower(document_name) LIKE '%registration fee%'"""
        ).fetchall()
        for row in rows:
            assert row['regulatory_source'] != 'rbi', \
                f"'{row['document_name']}' has regulatory_source=rbi — registration fees are a state subject"

    def test_no_null_document_names(self, db):
        count = db.execute("SELECT COUNT(*) FROM checklist_items WHERE document_name IS NULL OR document_name=''").fetchone()[0]
        assert count == 0

    def test_no_null_plain_explanations(self, db):
        count = db.execute("SELECT COUNT(*) FROM checklist_items WHERE plain_explanation IS NULL OR plain_explanation=''").fetchone()[0]
        assert count == 0

    def test_step_order_positive(self, db):
        count = db.execute("SELECT COUNT(*) FROM checklist_items WHERE step_order <= 0").fetchone()[0]
        assert count == 0

    def test_cost_min_lte_max(self, db):
        rows = db.execute(
            "SELECT id, document_name, approx_cost_min, approx_cost_max FROM checklist_items "
            "WHERE approx_cost_min IS NOT NULL AND approx_cost_max IS NOT NULL"
        ).fetchall()
        for row in rows:
            assert row['approx_cost_min'] <= row['approx_cost_max'], \
                f"cost_min > cost_max on '{row['document_name']}'"

    def test_minimum_items_per_tx_type(self, db):
        """Each tx type should have at least 8 items (incl. state-specific)."""
        for tx in ['home_loan', 'nri_account', 'property_registration', 'business_account']:
            count = db.execute(
                'SELECT COUNT(*) FROM checklist_items WHERE transaction_type=?', (tx,)
            ).fetchone()[0]
            assert count >= 8, f"{tx} only has {count} items"

    def test_source_notes_present(self, db):
        """All items should have a non-empty source_note."""
        count = db.execute(
            "SELECT COUNT(*) FROM checklist_items WHERE source_note IS NULL OR source_note=''"
        ).fetchone()[0]
        assert count == 0, f"{count} items have no source_note"


# ──────────────────────────────────────────────────────────────
# 4. Data access layer
# ──────────────────────────────────────────────────────────────

class TestDataAccess:
    def test_get_checklist_kerala_home_loan(self, app):
        from app.data.access import get_checklist
        with app.app_context():
            items = get_checklist('home_loan', 'kerala')
        assert len(items) >= 10
        sources = {i['state'] for i in items}
        assert None in sources    # national items included
        assert 'kerala' in sources  # state-specific included

    def test_get_checklist_maharashtra_property(self, app):
        from app.data.access import get_checklist
        with app.app_context():
            items = get_checklist('property_registration', 'maharashtra')
        assert len(items) >= 10
        assert any(i['state'] == 'maharashtra' for i in items)
        assert not any(i['state'] == 'kerala' for i in items)

    def test_get_checklist_nri_no_state(self, app):
        from app.data.access import get_checklist
        with app.app_context():
            items = get_checklist('nri_account', None)
        assert len(items) >= 8
        assert all(i['state'] is None for i in items)

    def test_get_checklist_ordered_by_step(self, app):
        from app.data.access import get_checklist
        with app.app_context():
            items = get_checklist('nri_account', None)
        orders = [i['step_order'] for i in items]
        assert orders == sorted(orders), "Items not ordered by step_order"

    def test_search_dataset_finds_encumbrance(self, app):
        from app.data.access import search_dataset
        with app.app_context():
            results = search_dataset('Encumbrance', 'home_loan')
        assert len(results) > 0
        assert any('encumbrance' in r['document_name'].lower() for r in results)

    def test_search_dataset_finds_stamp_duty(self, app):
        from app.data.access import search_dataset
        with app.app_context():
            results = search_dataset('stamp duty')
        assert len(results) > 0

    def test_search_dataset_no_results_graceful(self, app):
        from app.data.access import search_dataset
        with app.app_context():
            results = search_dataset('zzznomatchxxx')
        assert results == []


# ──────────────────────────────────────────────────────────────
# 5. AI layer — live provider test + fallback chain
# ──────────────────────────────────────────────────────────────

class TestAILayer:
    def test_explain_endpoint_returns_200(self, client):
        r = client.post('/api/ai/explain',
                        data=json.dumps({'term': 'PAN Card', 'transaction_type': 'home_loan'}),
                        content_type='application/json')
        assert r.status_code == 200

    def test_explain_response_has_required_fields(self, client):
        r = client.post('/api/ai/explain',
                        data=json.dumps({'term': 'PAN Card', 'transaction_type': 'home_loan'}),
                        content_type='application/json')
        d = r.get_json()
        assert 'explanation' in d
        assert 'source' in d

    def test_explain_source_is_valid(self, client):
        r = client.post('/api/ai/explain',
                        data=json.dumps({'term': 'PAN Card', 'transaction_type': 'home_loan'}),
                        content_type='application/json')
        d = r.get_json()
        assert d['source'] in ('openrouter', 'nvidia_nim', 'static_fallback')

    def test_explain_explanation_not_empty(self, client):
        r = client.post('/api/ai/explain',
                        data=json.dumps({'term': 'Encumbrance Certificate', 'transaction_type': 'home_loan'}),
                        content_type='application/json')
        d = r.get_json()
        assert len(d.get('explanation', '')) > 20

    def test_explain_missing_term_returns_400(self, client):
        r = client.post('/api/ai/explain',
                        data=json.dumps({'transaction_type': 'home_loan'}),
                        content_type='application/json')
        assert r.status_code == 400

    def test_explain_empty_term_returns_400(self, client):
        r = client.post('/api/ai/explain',
                        data=json.dumps({'term': '', 'transaction_type': 'home_loan'}),
                        content_type='application/json')
        assert r.status_code == 400

    def test_static_fallback_works_without_keys(self, app):
        """Simulate no API keys — static fallback must always return something."""
        from app.ai.client import generate
        from app.data.access import search_dataset

        orig_or  = os.environ.pop('OPENROUTER_API_KEY', None)
        orig_nim = os.environ.pop('NVIDIA_NIM_API_KEY', None)
        try:
            with app.app_context():
                ctx = search_dataset('Encumbrance Certificate', 'home_loan')
                result = generate('Encumbrance Certificate', ctx, max_tokens=200)
            assert result['source'] == 'static_fallback'
            assert len(result['explanation']) > 10
        finally:
            if orig_or:  os.environ['OPENROUTER_API_KEY']  = orig_or
            if orig_nim: os.environ['NVIDIA_NIM_API_KEY'] = orig_nim

    def test_live_ai_call_if_key_present(self, app):
        """The chain must always return usable prose, online or not.

        This deliberately does not assert that a live provider answered. Keys
        expire, free tiers run out of credit, and a test that demands a 200 from
        OpenRouter is a test that fails for reasons unrelated to the code. What
        matters is that whatever happens upstream, the caller still gets
        something it can render.
        """
        if not os.environ.get('OPENROUTER_API_KEY'):
            pytest.skip("No OPENROUTER_API_KEY set")
        from app.ai.client import generate
        from app.data.access import search_dataset
        with app.app_context():
            ctx = search_dataset('FEMA Declaration', 'nri_account')
            result = generate('FEMA Declaration', ctx, max_tokens=150)
        assert result['source'] in ('openrouter', 'nvidia_nim', 'static_fallback')
        assert len(result['explanation']) > 20

    def test_explain_multiple_terms(self, client):
        terms = [
            ('Stamp Duty', 'property_registration'),
            ('Form 16', 'home_loan'),
            ('GST Registration Certificate', 'business_account'),
            ('Valid Indian Passport', 'nri_account'),
        ]
        for term, tx in terms:
            r = client.post('/api/ai/explain',
                            data=json.dumps({'term': term, 'transaction_type': tx}),
                            content_type='application/json')
            d = r.get_json()
            assert r.status_code == 200, f"Failed for '{term}'"
            assert len(d.get('explanation', '')) > 10, f"Empty explanation for '{term}'"


# ──────────────────────────────────────────────────────────────
# 6. Data API blueprint
# ──────────────────────────────────────────────────────────────

class TestDataAPI:
    def test_checklist_api_home_loan_kerala(self, client):
        r = client.get('/api/data/checklist/home_loan?state=kerala')
        assert r.status_code == 200
        data = r.get_json()
        assert isinstance(data, list)
        assert len(data) >= 10

    def test_checklist_api_nri(self, client):
        r = client.get('/api/data/checklist/nri_account')
        assert r.status_code == 200
        data = r.get_json()
        assert len(data) >= 8

    def test_checklist_api_returns_json(self, client):
        r = client.get('/api/data/checklist/business_account?state=maharashtra')
        assert 'application/json' in r.content_type


# ──────────────────────────────────────────────────────────────
# 7. Template rendering quality checks
# ──────────────────────────────────────────────────────────────
