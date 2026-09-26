from flask import Blueprint, jsonify
from .access import get_checklist

data_bp = Blueprint('data_bp', __name__)

@data_bp.route('/checklist/<transaction_type>')
def checklist_api(transaction_type):
    from flask import request
    state = request.args.get('state')
    items = get_checklist(transaction_type, state)
    return jsonify(items)
