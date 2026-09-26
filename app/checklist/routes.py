from flask import Blueprint, render_template, request, session
from ..data.access import get_checklist

checklist_bp = Blueprint('checklist', __name__)

TRANSACTION_LABELS = {
    'home_loan': 'Home Loan Application',
    'nri_account': 'NRI Account Opening (NRE/NRO)',
    'property_registration': 'Property Sale Deed Registration',
    'business_account': 'Business Current Account Opening',
}
STATE_LABELS = {
    'kerala': 'Kerala',
    'maharashtra': 'Maharashtra',
}
STATE_DEPENDENT = ['home_loan', 'property_registration', 'business_account']

@checklist_bp.route('/')
def index():
    return render_template('index.html',
                           transaction_labels=TRANSACTION_LABELS,
                           state_labels=STATE_LABELS,
                           state_dependent=STATE_DEPENDENT)

@checklist_bp.route('/checklist')
def checklist():
    tx = request.args.get('transaction_type', '')
    state = request.args.get('state', None)
    if tx not in TRANSACTION_LABELS:
        return render_template('index.html',
                               error="Please select a valid transaction type.",
                               transaction_labels=TRANSACTION_LABELS,
                               state_labels=STATE_LABELS,
                               state_dependent=STATE_DEPENDENT)
    items = get_checklist(tx, state)
    return render_template('checklist.html',
                           items=items,
                           transaction_type=tx,
                           transaction_label=TRANSACTION_LABELS.get(tx, tx),
                           state=state,
                           state_label=STATE_LABELS.get(state, ''),
                           total=len(items))
