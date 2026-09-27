"""Smoke tests: the app boots and the core routes answer.

Deliberately thin. The substantive coverage lives in test_research.py
(research agent, cache, honesty rules, search backend) and
test_comprehensive.py (legacy dataset integrity, AI fallback chain, UI
structure). This file exists so a broken import or a failed app factory is
caught in under a second, before the slower suites run.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


@pytest.fixture
def no_network_ai():
    """Stub the AI provider so no test in this file makes a network call."""
    import app.ai.routes as ai_routes
    original = ai_routes.generate
    ai_routes.generate = lambda term, rows, max_tokens=300: {
        "explanation": "Stubbed explanation for %r, long enough to render."
                       % term,
        "source": "openrouter",
    }
    yield
    ai_routes.generate = original


def test_index(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Kaagaz' in resp.data


def test_about(client):
    resp = client.get('/about')
    assert resp.status_code == 200


def test_checklist_home_loan_kerala(client):
    resp = client.get(
        '/checklist?transaction_type=home+loan&state=Kerala&residency=resident')
    assert resp.status_code == 200
    assert b'Kaagaz' in resp.data


def test_checklist_nri_account(client):
    resp = client.get(
        '/checklist?transaction_type=nri+account&bank=State+Bank+of+India'
        '&residency=nri')
    assert resp.status_code == 200


def test_checklist_rejects_an_empty_transaction(client):
    resp = client.get('/checklist?transaction_type=')
    assert resp.status_code == 400
    assert b'Tell us what you' in resp.data


def test_ai_explain(client, no_network_ai):
    resp = client.post('/api/ai/explain', json={
        'term': 'Encumbrance Certificate', 'transaction_type': 'home_loan',
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'explanation' in data
    assert data['source'] in ('openrouter', 'nvidia_nim', 'static_fallback')
    assert len(data['explanation']) > 20


def test_ai_explain_requires_a_term(client, no_network_ai):
    resp = client.post('/api/ai/explain', json={'term': '  '})
    assert resp.status_code == 400
