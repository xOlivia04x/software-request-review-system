# Software Request Review System

An original educational Python, SQLite, and Streamlit application for submitting and reviewing enterprise software requests. All sample organizations and data are fictional.

## Features
- Submit software requests with business justification, estimated cost, security considerations, and integration requirements
- Persist requests in a local SQLite database
- Filter requests by review status
- Record architecture reviews with reviewer names, security/integration findings, decision notes, and timestamps
- Track previous and new statuses in a review-history table
- Dashboard metrics for total, pending, in-review, and approved requests
- Automated database tests

## Run locally

Requires Python 3.9 or newer.

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

On Windows, replace `python` with `py` if needed. Streamlit typically opens at http://localhost:8501.

For the original command-line demonstration:

```bash
python main.py
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Architecture
- `app.py`: Streamlit forms, dashboard, request browsing, and review history
- `database.py`: SQLite schema, validation, and database operations
- `main.py`: original command-line demo
- `tests/test_database.py`: automated tests using temporary SQLite databases
- `requirements.txt`: Streamlit dependency

On startup, `initialize_database()` creates missing tables without deleting existing requests. Reviews update a request's status and append a history entry in one database transaction. The local `requests.db` file is excluded from Git.

## Limitations
This is a portfolio demonstration, **not a production approval or security assessment system**. It has no authentication, role-based permissions, formal security evaluation, or tamper-proof audit log. Reviewer names are entered manually. Review history is illustrative and should not be relied on for compliance.
