import json
from flask import Blueprint, request, jsonify
from .client import generate
from ..data.access import search_dataset

ai_bp = Blueprint('ai_bp', __name__)

@ai_bp.route('/explain', methods=['POST'])
def explain():
    data = request.get_json(force=True)
    term = data.get('term', '').strip()
    tx_type = data.get('transaction_type', '').strip()
    if not term:
        return jsonify({'error': 'term is required'}), 400
    context_rows = search_dataset(term, tx_type)
    result = generate(term, context_rows, max_tokens=300)
    return jsonify(result)
