"""SQLite persistence for software requests and architecture review history."""
import math
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name('requests.db')
STATUSES = ('Pending', 'In Review', 'Approved', 'Rejected')


def connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute('PRAGMA foreign_keys = ON')
    return connection


def initialize_database():
    """Create tables if missing. Existing requests are preserved."""
    with connect() as connection:
        connection.execute('''
            CREATE TABLE IF NOT EXISTS software_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                software_name TEXT NOT NULL,
                department TEXT NOT NULL,
                justification TEXT NOT NULL,
                estimated_cost REAL NOT NULL CHECK (estimated_cost >= 0),
                security_notes TEXT NOT NULL DEFAULT '',
                integration_notes TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'Pending'
                    CHECK (status IN ('Pending', 'In Review', 'Approved', 'Rejected')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        connection.execute('''
            CREATE TABLE IF NOT EXISTS review_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_id INTEGER NOT NULL,
                reviewer TEXT NOT NULL CHECK (length(trim(reviewer)) > 0),
                previous_status TEXT NOT NULL,
                new_status TEXT NOT NULL,
                security_findings TEXT NOT NULL DEFAULT '',
                integration_findings TEXT NOT NULL DEFAULT '',
                decision_notes TEXT NOT NULL CHECK (length(trim(decision_notes)) > 0),
                reviewed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (request_id) REFERENCES software_requests(id)
            )
        ''')


def add_request(software_name, department, justification, estimated_cost,
                security_notes='', integration_notes=''):
    if not all(isinstance(v, str) and v.strip() for v in
               (software_name, department, justification)):
        raise ValueError('Software name, department, and justification are required.')
    try:
        cost = float(estimated_cost)
    except (TypeError, ValueError, OverflowError):
        raise ValueError('Estimated cost must be a valid number.') from None
    if not math.isfinite(cost) or cost < 0:
        raise ValueError('Estimated cost must be a finite nonnegative number.')
    with connect() as connection:
        cursor = connection.execute('''
            INSERT INTO software_requests
                (software_name, department, justification, estimated_cost,
                 security_notes, integration_notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (software_name.strip(), department.strip(), justification.strip(), cost,
              security_notes.strip(), integration_notes.strip()))
        return cursor.lastrowid


def get_requests():
    with connect() as connection:
        rows = connection.execute('SELECT * FROM software_requests ORDER BY id DESC').fetchall()
    return [dict(row) for row in rows]


def get_review_history(request_id):
    with connect() as connection:
        rows = connection.execute('''
            SELECT * FROM review_history WHERE request_id = ?
            ORDER BY id DESC
        ''', (request_id,)).fetchall()
    return [dict(row) for row in rows]


def add_review(request_id, reviewer, new_status, decision_notes,
               security_findings='', integration_findings=''):
    """Atomically update request status and append a review-history record."""
    if new_status not in STATUSES:
        raise ValueError('Invalid review status.')
    if not isinstance(reviewer, str) or not reviewer.strip():
        raise ValueError('Reviewer name is required.')
    if not isinstance(decision_notes, str) or not decision_notes.strip():
        raise ValueError('Decision notes are required.')
    with connect() as connection:
        request = connection.execute(
            'SELECT status FROM software_requests WHERE id = ?', (request_id,)
        ).fetchone()
        if request is None:
            raise ValueError('Request not found.')
        previous_status = request['status']
        connection.execute(
            'UPDATE software_requests SET status = ? WHERE id = ?',
            (new_status, request_id)
        )
        cursor = connection.execute('''
            INSERT INTO review_history
                (request_id, reviewer, previous_status, new_status,
                 security_findings, integration_findings, decision_notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (request_id, reviewer.strip(), previous_status, new_status,
              security_findings.strip(), integration_findings.strip(),
              decision_notes.strip()))
        return cursor.lastrowid


def update_request_status(request_id, status):
    """Compatibility wrapper for the original command-line/demo interface."""
    return add_review(request_id, 'Demo reviewer', status,
                      'Status updated through the compatibility interface.')


if __name__ == '__main__':
    initialize_database()
    print(f'Database initialized: {DB_PATH.name}')
