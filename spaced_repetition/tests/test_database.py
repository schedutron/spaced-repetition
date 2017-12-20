#!/usr/bin/env python3
import datetime
import unittest
from urllib import parse

import psycopg2
from spaced_repetition.database import *
from spaced_repetition.env import *

class TestDatabase(unittest.TestCase):
    url = parse.urlparse(DATABASE_URL)
    conn = db_connect(url)
    dsn = get_dsn(conn)
    
    def test_db_name(self):
        self.assertEqual(self.dsn['dbname'], 'learn')
    
    def test_get_last_rev_with_id_and_level(self):
        cur = self.conn.cursor()
        cur = get_last_rev_with_id_and_level(cur)
        for row in cur:
            self.assertEqual(type(row[0]), int)

            self.assertEqual(type(row[1]),
                type(datetime.datetime.now().date())
                )
            self.assertEqual(type(row[2]), int)


if __name__ == "__main__":
    unittest.main()
