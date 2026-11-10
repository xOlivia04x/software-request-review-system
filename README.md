# Software Request Review System

An original Python and SQLite project for tracking enterprise software requests and documenting review considerations.

## Current features

- SQLite database for software requests
- Validated request creation
- Retrieval of saved requests
- Initial request status: Pending
- Example command-line demonstration

## Run

Requires Python 3.9 or newer. No third-party dependencies for this initial version.

```bash
python main.py
```

The program creates a local `requests.db` file, inserts an example request on the first run, and lists saved requests. The database file is ignored by Git.

## Next milestones

- Review status updates and history
- Streamlit web dashboard
- Filtering and reporting
- Automated tests

## Notes

All example organizations and requests are fictional. This is a portfolio demonstration, not a production approval or security assessment system.
