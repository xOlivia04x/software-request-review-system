"""Run with: python -m unittest discover -s tests -v"""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import database


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path_patch = patch.object(database, 'DB_PATH', Path(self.temp.name) / 'test.db')
        self.path_patch.start()
        database.initialize_database()

    def tearDown(self):
        self.path_patch.stop()
        self.temp.cleanup()

    def test_create_and_review_request(self):
        rid = database.add_request('Analytics Tool', 'Finance', 'Reporting', 1200)
        review_id = database.add_review(rid, 'Test Reviewer', 'Approved',
                                        'Approved for pilot', 'Access review needed',
                                        'CSV import supported')
        self.assertGreater(review_id, 0)
        self.assertEqual(database.get_requests()[0]['status'], 'Approved')
        history = database.get_review_history(rid)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['previous_status'], 'Pending')
        self.assertEqual(history[0]['new_status'], 'Approved')
        self.assertEqual(history[0]['reviewer'], 'Test Reviewer')

    def test_reject_invalid_review_without_changing_status(self):
        rid = database.add_request('Tool', 'IT', 'Needed', 10)
        for kwargs in [dict(reviewer='', new_status='Approved', decision_notes='OK'),
                       dict(reviewer='Sam', new_status='Unknown', decision_notes='OK'),
                       dict(reviewer='Sam', new_status='Approved', decision_notes='')]:
            with self.assertRaises(ValueError):
                database.add_review(rid, **kwargs)
        self.assertEqual(database.get_requests()[0]['status'], 'Pending')
        self.assertEqual(database.get_review_history(rid), [])

    def test_missing_request_and_cost_validation(self):
        with self.assertRaises(ValueError):
            database.add_review(999, 'Sam', 'Approved', 'OK')
        with self.assertRaises(ValueError):
            database.add_request('Tool', 'IT', 'Needed', -1)

    def test_initialize_does_not_erase_existing_data(self):
        rid = database.add_request('Tool', 'IT', 'Needed', 0)
        database.initialize_database()
        self.assertEqual(database.get_requests()[0]['id'], rid)


if __name__ == '__main__':
    unittest.main()
