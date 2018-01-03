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
    url = parse.urlparse(TEST_DATABASE_URL)
    conn = db_connect(url)
    dsn = get_dsn(conn)
    cur = conn.cursor()

    def test_db_name(self):
        self.assertEqual(self.dsn['dbname'], 'pavjstve')

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
        for row in self.cur:  # Just one row.
            if row[0] == 0:
                title = "Polynomial Multiplication"
                add_date = datetime.datetime.strptime(
                    '19122017', '%d%m%Y'
                    ).date()
            elif row[0] == 1:
                title = "Design of Computer Programs"
                add_date = datetime.datetime.strptime(
                    '20102017', '%d%m%Y'
                    ).date()
            self.assertEqual(row[1], title)
            self.assertEqual(row[4], add_date)
    
    def test_set_for_next_date(self):
        pass
    
    def test_init_test_db(self):
        pass
    
    def test_insert_rows(self):
        insert_row(self.cur,
                   'notebooks',
                   '(title, begin_date, total_entries)',
                   ('The Book', datetime.datetime.now().date(), 9)
                  )
        self.cur.execute(
            "select title, begin_date, total_entries from notebooks"
            " where title='The Book'")
        row = next(self.cur)
        self.cur.execute("delete from notebooks where title='The Book'")
        self.cur.connection.commit()
        self.assertEqual(('The Book', datetime.datetime.now().date(), 9), row)


if __name__ == "__main__":
    unittest.main()
