#!/usr/bin/env python3
"""Tests for database interface functions."""
# Clone the current database instance for testing.
import datetime
import unittest
from urllib import parse

from spaced_repetition.database import *
from spaced_repetition.env import *

class TestDatabase(unittest.TestCase):
    """Database interface tests."""
    url = parse.urlparse(DATABASE_URL)
    conn = db_connect(url)
    dsn = get_dsn(conn)
    cur = conn.cursor()

    def test_db_name(self):
        self.assertEqual(self.dsn['dbname'], 'learn')

    def test_get_last_rev_with_id_and_level(self):
        self.cur = get_last_rev_with_id_and_level(self.cur)
        for row in self.cur:
            self.assertEqual(type(row[0]), int)

            self.assertEqual(type(row[1]),
                             type(datetime.datetime.now().date())
                            )
            self.assertEqual(type(row[2]), int)

    def test_get_rows_for_ids(self):
        self.cur = get_rows_for_ids(self.cur, [0, 1])
        count = 0
        for row in self.cur:  # Just one row.
            if count == 0:
                id_val = 0
                title = "Polynomial Multiplication"
            else:
                id_val = 1
                title = "Design of Computer Programs"
            self.assertEqual(row[0], id_val)
            self.assertEqual(row[1], title)
            count += 1
    
    def test_set_for_next_date(self):
        pass


if __name__ == "__main__":
    unittest.main()
