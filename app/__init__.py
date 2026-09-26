import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

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

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-me')
    app.config['DATABASE'] = os.path.join(app.instance_path, 'kaagaz.db')

    app.jinja_env.filters['format_inr'] = _format_inr

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .checklist import checklist_bp
    from .ai import ai_bp
    from .data import data_bp
    app.register_blueprint(checklist_bp)
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.register_blueprint(data_bp, url_prefix='/api/data')

    with app.app_context():
        from .data.db_seed import seed_db
        seed_db(app)

    return app
