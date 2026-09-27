import os
import tempfile

from flask import Flask
from dotenv import load_dotenv

load_dotenv()

# Databases that are in memory only. Set by the deployment fallbacks below when
# no writable file location could be found, so the app still runs (degraded and
# clearly labelled) rather than failing at import time.
_TMP_DB = None


def _format_inr(value):
    """Format an integer as Indian-locale number string (e.g. 100000 → 1,00,000)."""
    try:
        value = int(value)
    except (TypeError, ValueError):
        return str(value)
    if value < 0:
        return "-" + _format_inr(-value)
    s = str(value)
    if len(s) <= 3:
        return s
    # Last 3 digits, then groups of 2
    result = s[-3:]
    s = s[:-3]
    while s:
        result = s[-2:] + "," + result
        s = s[:-2]
    return result


def _is_writable_dir(path):
    """Can we create a file in this directory?

    Deliberately checks the DIRECTORY, not the target file. An earlier version
    probed the file itself with `open(candidate, 'a')`, which *created* it — and
    `db_seed.seed_db` then saw a file already present, concluded it had been
    seeded, and returned without creating any tables. Every fresh clone would
    have started with a database containing no `checklist_items` table at all,
    and the first checklist page would 500. Caught by deleting the database and
    starting again, which is the only way this kind of bug is ever caught.
    """
    if not os.path.isdir(path):
        try:
            os.makedirs(path)
        except OSError:
            return False
    return os.access(path, os.W_OK | os.X_OK)


def _resolve_database_path(instance_path):
    """Pick a writable location for the SQLite file.

    Order of preference:

      1. ``DATABASE_PATH`` — explicit override, always wins.
      2. ``instance/`` — the Flask-idiomatic location, used in development.
      3. ``/tmp/`` — on serverless platforms (Vercel, Lambda) the deployment
         bundle is read-only and only ``/tmp`` is writable. Without this the app
         dies at import time on the first write.
      4. an in-memory database — last resort, so the process still serves
         requests and reports its own degraded state rather than 500-ing.

    This function must not create the file it returns; see _is_writable_dir.
    """
    global _TMP_DB

    override = os.environ.get('DATABASE_PATH', '').strip()
    if override:
        return override

    candidate = os.path.join(instance_path, 'kaagaz.db')
    if _is_writable_dir(instance_path):
        return candidate

    fallback_dir = tempfile.gettempdir()
    if _is_writable_dir(fallback_dir):
        return os.path.join(fallback_dir, 'kaagaz.db')

    _TMP_DB = ':memory:'
    return _TMP_DB


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-me')
    app.config['DATABASE'] = _resolve_database_path(app.instance_path)
    # Anything outside instance/ is /tmp or memory, so it does not survive a
    # cold start. The UI and the health endpoint report this rather than
    # pretending the cache is durable.
    app.config['DATABASE_IS_EPHEMERAL'] = not os.path.abspath(
        app.config['DATABASE']
    ).startswith(os.path.abspath(app.instance_path))
    # Serverless platforms also destroy /tmp on cold start, so the research
    # cache must be able to rebuild itself. See _ensure_research_seed().
    app.config['SERVERLESS'] = bool(
        os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME')
    )

    app.jinja_env.filters['format_inr'] = _format_inr

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .checklist import checklist_bp
    from .ai import ai_bp
    from .data import data_bp
    from .research.routes import research_bp
    from .research import cache as research_cache
    app.register_blueprint(checklist_bp)
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.register_blueprint(data_bp, url_prefix='/api/data')
    app.register_blueprint(research_bp, url_prefix='/api/research')

    with app.app_context():
        from .data.db_seed import seed_db
        seed_db(app)
        # Phase 2: research cache lives alongside the Phase-1 seed dataset
        research_cache.init_schema(app)
        _ensure_research_seed(app)

    return app


def _ensure_research_seed(app):
    """Populate the research cache if it is empty.

    On a normal machine this is a no-op — you pre-warm with
    ``scripts/preseed``. But on a serverless cold start the SQLite file lives
    in /tmp and is gone, so without this the deployed instance would answer
    every question with a 15-40 second research call and look broken. The seed
    data is bundled, so the demo cases come back instantly on their own.
    """
    from .research import cache as research_cache
    try:
        stats = research_cache.stats(app)
        if stats.get('entries', 0) > 0:
            return
    except Exception:
        return  # never let cache bookkeeping break startup

    try:
        from scripts.preseed import seed_all
        seeded, _skipped = seed_all(app, force=False, verbose=False)
        if seeded:
            app.logger.info(
                'Research cache was empty; auto-seeded %d entries. '
                'Set DATABASE_PATH to a persistent volume to keep them.',
                seeded,
            )
    except Exception as exc:  # noqa: BLE001
        app.logger.warning('Could not auto-seed the research cache: %s', exc)
