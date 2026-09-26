import sqlite3
import json
import os

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS checklist_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_type TEXT NOT NULL,
    state TEXT,
    step_order INTEGER NOT NULL,
    document_name TEXT NOT NULL,
    plain_explanation TEXT,
    where_to_obtain TEXT,
    approx_cost_min INTEGER,
    approx_cost_max INTEGER,
    approx_time_days INTEGER,
    depends_on TEXT,
    regulatory_source TEXT,
    source_note TEXT
)
"""

def seed_db(app):
    db_path = app.config['DATABASE']
    if os.path.exists(db_path):
        return  # already seeded
    
    data_dir = os.path.join(os.path.dirname(__file__))
    dataset_path = os.path.join(data_dir, 'dataset.json')
    
    conn = sqlite3.connect(db_path)
    conn.execute(CREATE_TABLE)
    
    with open(dataset_path, 'r') as f:
        items = json.load(f)
    
    for item in items:
        conn.execute(
            """INSERT INTO checklist_items
               (transaction_type, state, step_order, document_name, plain_explanation,
                where_to_obtain, approx_cost_min, approx_cost_max, approx_time_days,
                depends_on, regulatory_source, source_note)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                item.get('transaction_type'),
                item.get('state'),
                item.get('step_order'),
                item.get('document_name'),
                item.get('plain_explanation'),
                item.get('where_to_obtain'),
                item.get('approx_cost_min'),
                item.get('approx_cost_max'),
                item.get('approx_time_days'),
                item.get('depends_on'),
                item.get('regulatory_source'),
                item.get('source_note'),
            )
        )
    conn.commit()
    conn.close()
