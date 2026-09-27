"""
Kaagaz — page routes.

The picker is now a free-text question rather than a four-item menu, because
the product's claim is that it can answer for anything. Everything below is
thin: all the real logic lives in app/research/agent.py.
"""

from flask import (Blueprint, current_app, redirect, render_template, request,
                   url_for)

from ..research import agent, cache as cache_mod, refdata
from ..research.synthesize import REGULATORY_LABELS

checklist_bp = Blueprint('checklist', __name__)

# Kept so the Phase-1 four still resolve to the same friendly labels.
TRANSACTION_LABELS = {
    'home_loan': 'Home loan',
    'nri_account': 'NRI account opening (NRE / NRO)',
    'property_registration': 'Property registration',
    'business_account': 'Business current account opening',
}

# Demo-safe starting points, shown on the picker. These are exactly the cases
# that are pre-warmed, so clicking one answers instantly. Each carries the
# residency status and state it was researched under, because both change the
# answer for most of these. tests/test_research.py::TestDemoIsPreWarmed
# asserts that every one of these resolves to a cache hit — a seed whose chip
# misses is a broken demo, and that is not a mistake to make twice.
EXAMPLES = [
    ('home loan', 'HDFC Bank', 'resident', '',
     'Home loan · HDFC Bank', '14 documents, rate band included'),
    ('home loan', 'State Bank of India', 'nri', '',
     'Home loan · SBI, as an NRI',
     '10 documents, includes work permit and attestation'),
    ('study abroad loan', 'State Bank of India', 'all_nri', '',
     'Education loan · study abroad', '13 documents, all-NRI household'),
    ('loan against fixed deposit', 'State Bank of India', 'resident', '',
     'Loan against FD · SBI', '6 documents, spread pricing'),
    ('fd as guarantee', 'State Bank of India', 'resident', '',
     'FD as a guarantee',
     'The contrast case — and why it is not the same thing'),
    ('nri account', 'State Bank of India', 'nri', '',
     'NRI account · NRE / NRO', '9 documents, FEMA and attestation'),
    ('property registration', '', 'not_applicable', 'Kerala',
     'Property registration · Kerala', '13 documents, stamp act vs registrar'),
    ('business current account', 'ICICI Bank', 'not_applicable', '',
     'Business current account · ICICI', '12 documents, company structure'),
    ('gold loan', 'State Bank of India', 'resident', '',
     'Gold loan · SBI', '8 documents, post-2025 RBI directions'),
    ('mudra loan', '', 'resident', '',
     'Mudra loan', '11 documents, by category'),
]


def _clean_params(source=None):
    """Pull the four research inputs out of the query string."""
    source = source if source is not None else request.args
    return {
        'transaction_type': (source.get('transaction_type') or '').strip(),
        'bank': (source.get('bank') or '').strip(),
        'state': (source.get('state') or '').strip(),
        'residency': (source.get('residency') or 'resident').strip(),
    }


@checklist_bp.route('/')
def index():
    app = current_app._get_current_object()
    return render_template(
        'index.html',
        popular_categories=[(c, refdata.CATEGORIES.get(c, c))
                            for c in refdata.POPULAR_CATEGORIES],
        bank_names=[name for name, _ in refdata.bank_options()],
        state_names=sorted(set(refdata.STATES.values())),
        residency_options=[(k, refdata.RESIDENCY[k])
                           for k in refdata.RESIDENCY_ORDER],
        examples=EXAMPLES,
        stats=cache_mod.stats(app),
        error=request.args.get('error'),
    )


@checklist_bp.route('/checklist')
def checklist():
    """Cache-first. On a miss we do NOT research inline — we render the
    researching view and let the browser drive the job, so the progress is
    real and visible rather than a blocked request."""
    app = current_app._get_current_object()
    params = _clean_params()

    try:
        req = agent.parse_request(params)
    except agent.ResearchFailed as exc:
        return render_template(
            'index.html',
            popular_categories=[(c, refdata.CATEGORIES.get(c, c))
                                for c in refdata.POPULAR_CATEGORIES],
            bank_names=[name for name, _ in refdata.bank_options()],
            state_names=sorted(set(refdata.STATES.values())),
            residency_options=[(k, refdata.RESIDENCY[k])
                               for k in refdata.RESIDENCY_ORDER],
            examples=EXAMPLES,
            stats=cache_mod.stats(app),
            error=exc.message,
        ), 400

    cache_key = cache_mod.make_cache_key(
        req['transaction_type'], req['bank'], req['residency'], req['state']
    )
    hit = cache_mod.get_fresh(app, cache_key)

    if hit is None:
        # Miss or stale. The researching view takes it from here.
        return render_template('researching.html', request=req,
                               cache_key=cache_key)

    cache_mod.touch(app, cache_key)
    req['cache_key'] = cache_key
    payload = agent._decorate(req, hit['answer'], hit)
    payload.update(_view_context(hit, cache='hit', just=params and
                                 request.args.get('just')))
    return render_template('checklist.html', **payload)


@checklist_bp.route('/about')
def about():
    app = current_app._get_current_object()
    return render_template('about.html', stats=cache_mod.stats(app))


@checklist_bp.route('/favicon.ico')
def favicon():
    """Chrome requests /favicon.ico regardless of the SVG <link>, so send it
    to the real mark rather than logging a 404 on every page view."""
    return redirect(url_for('static', filename='favicon.svg'), code=301)


# Which custom icon represents each regulatory bucket. Kept beside the label so
# the glyph and the wording can never drift apart.
GOV_ICONS = {
    'rbi': 'seal',
    'state_stamp_act': 'stamp',
    'registrar': 'registry',
    'bank_internal': 'shop',
}

# Short forms for the legend strip; the per-item label uses the fuller wording.
# Apostrophe-free, for the reason noted in synthesize.REGULATORY_LABELS.
GOV_LEGEND_LABELS = {
    'rbi': 'RBI rules',
    'state_stamp_act': 'State stamp act',
    'registrar': 'Registrar / state',
    'bank_internal': 'Bank policy',
}


def _view_context(entry, cache='miss', just=False):
    """Shared template context for the result view."""
    sources = []
    for source in (entry.get('answer', {}).get('sources')
                   or entry.get('source_urls') or []):
        if isinstance(source, str):
            url = source
            host = ''
            for prefix in ('https://', 'http://'):
                if url.startswith(prefix):
                    url = url[len(prefix):]
                    break
            host = url.split('/')[0].replace('www.', '')
            sources.append({'url': source, 'title': '', 'host': host})
        else:
            url = source.get('url', '')
            host = source.get('host', '')
            if not host and url:
                host = url.split('//')[-1].split('/')[0].replace('www.', '')
            sources.append({'url': url, 'title': source.get('title', ''),
                            'host': host})
    return {
        'gov_labels': REGULATORY_LABELS,
        'gov_icons': GOV_ICONS,
        'legend_labels': GOV_LEGEND_LABELS,
        'sources': sources,
        'cache': cache,
        'just_researched': just == '1',
    }
