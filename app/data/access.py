import sqlite3
import os
from flask import g, current_app

def get_db(app=None):
    if app:
        db_path = app.config['DATABASE']
    else:
        db_path = current_app.config['DATABASE']
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def get_checklist(transaction_type: str, state: str = None) -> list:
    conn = get_db()
    try:
        if state:
            rows = conn.execute(
                """SELECT * FROM checklist_items
                   WHERE transaction_type = ?
                     AND (state = ? OR state IS NULL)
                   ORDER BY step_order""",
                (transaction_type, state)
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT * FROM checklist_items
                   WHERE transaction_type = ?
                     AND state IS NULL
                   ORDER BY step_order""",
                (transaction_type,)
            ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def search_dataset(term: str, transaction_type: str = None) -> list:
    conn = get_db()
    try:
        pattern = f"%{term}%"
        if transaction_type:
            rows = conn.execute(
                """SELECT * FROM checklist_items
                   WHERE (document_name LIKE ? OR plain_explanation LIKE ?)
                     AND transaction_type = ?
                   LIMIT 5""",
                (pattern, pattern, transaction_type)
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT * FROM checklist_items
                   WHERE document_name LIKE ? OR plain_explanation LIKE ?
                   LIMIT 5""",
                (pattern, pattern)
            ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()
