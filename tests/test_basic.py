import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_index(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Kaagaz' in resp.data

def test_checklist_home_loan_kerala(client):
    resp = client.get('/checklist?transaction_type=home_loan&state=kerala')
    assert resp.status_code == 200

def test_checklist_nri_account(client):
    resp = client.get('/checklist?transaction_type=nri_account')
    assert resp.status_code == 200

def test_ai_explain(client):
    resp = client.post('/api/ai/explain', json={'term': 'Encumbrance Certificate', 'transaction_type': 'home_loan'})
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'explanation' in data
    assert data['source'] in ('openrouter', 'nvidia_nim', 'static_fallback')
    assert len(data['explanation']) > 20
