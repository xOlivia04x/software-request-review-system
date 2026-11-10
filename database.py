"""SQLite persistence for the Software Request Review System."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name('requests.db')


def connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
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


def add_request(software_name, department, justification, estimated_cost,
                security_notes='', integration_notes=''):
    if not all(value.strip() for value in (software_name, department, justification)):
        raise ValueError('Software name, department, and justification are required.')
    cost = float(estimated_cost)
    if not 0 <= cost < float('inf'):
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
        rows = connection.execute('''
            SELECT * FROM software_requests ORDER BY id DESC
        ''').fetchall()
    return [dict(row) for row in rows]


if __name__ == '__main__':
    initialize_database()
    print(f'Database initialized: {DB_PATH.name}')


def update_request_status(request_id, status):
    """Update the review status of an existing software request."""
    allowed = {'Pending', 'In Review', 'Approved', 'Rejected'}
    if status not in allowed:
        raise ValueError('Invalid review status.')
    with connect() as connection:
        cursor = connection.execute(
            'UPDATE software_requests SET status = ? WHERE id = ?',
            (status, request_id)
        )
        if cursor.rowcount == 0:
            raise ValueError('Request not found.')
