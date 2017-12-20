#!/usr/bin/env python3
import datetime
import unittest
from urllib import parse

from spaced_repetition.env import *
from spaced_repetition.functions import *
from spaced_repetition import database

class TestFunctions(unittest.TestCase):
    url = parse.urlparse(DATABASE_URL)
    conn = database.db_connect(url)
    dsn = database.get_dsn(conn)

    def test_get_next_date(self):
        day = datetime.datetime.strptime('19081998', '%d%m%Y').date()
        next_day = datetime.datetime.strptime('20081998', '%d%m%Y').date()
        self.assertEqual(get_next_date(day, 1), next_day)

        today = datetime.datetime.now().date()
        tomorrow = today + datetime.timedelta(days=1)
        self.assertEqual(get_next_date(today, 1), tomorrow)
    
    def test_learn_today(self):
        cur = self.conn.cursor()
        self.assertEqual(type(learn_today(cur)), list)


if __name__ == '__main__':
    unittest.main()
