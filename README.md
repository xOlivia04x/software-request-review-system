# Software Request Review System

An original Python, SQLite, and Streamlit portfolio application for submitting and reviewing enterprise software requests. Uses fictional data; not a production security or approval system.

## Features
- Submit requests with business justification, estimated cost, security considerations, and integration requirements
- Save and retrieve requests using SQLite
- Browse and filter requests by review status
- Update status to Pending, In Review, Approved, or Rejected
- Dashboard metrics for request counts

## Run locally

Requires Python 3.9 or newer.

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

On Windows, replace `python` with `py` if needed. The application opens in your browser, typically at `http://localhost:8501`.

For the original command-line demo:

```bash
python main.py
```

The database (`requests.db`) is created locally and excluded from Git.

## Architecture
- `app.py`: Streamlit user interface
- `database.py`: SQLite schema and database operations
- `main.py`: original command-line demonstration
- `requirements.txt`: Streamlit dependency

## Limitations and future work
This educational application does not implement authentication, authorization, audit trails, or formal security assessment. Review statuses are for demonstration only. Planned enhancements include reviewer accounts, decision notes, and automated tests.
