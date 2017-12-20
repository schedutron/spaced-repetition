#!/usr/bin/env python3
import contextlib
import datetime
import unittest
from io import StringIO
from urllib import parse

from spaced_repetition.env import *
from spaced_repetition.functions import *
from spaced_repetition import database

class TestFunctions(unittest.TestCase):
    url = parse.urlparse(DATABASE_URL)
    conn = database.db_connect(url)
    dsn = database.get_dsn(conn)
    cur = conn.cursor()

    def test_get_next_date(self):
        day = datetime.datetime.strptime('19081998', '%d%m%Y').date()
        next_day = datetime.datetime.strptime('20081998', '%d%m%Y').date()
        self.assertEqual(get_next_date(day, 1), next_day)

        today = datetime.datetime.now().date()
        tomorrow = today + datetime.timedelta(days=1)
        self.assertEqual(get_next_date(today, 1), tomorrow)
    
    def test_learn_today(self):
        self.assertEqual(type(learn_today(self.cur)), list)
    
    def test_get_colnames(self):
        self.cur.execute("SELECT id, title, add_date from to_learn")
        self.assertEqual(get_colnames(self.cur), ['id', 'title', 'add_date'])
    
    def test_display_rows(self):
        out = StringIO()
        self.cur.execute(
            "SELECT id, title, add_date from to_learn WHERE id IN (0, 1)"
            )
        with contextlib.redirect_stdout(out):
            display_rows(self.cur)
        output = out.getvalue()
        expected = "id title                       add_date   \n\n"\
                   "0  Polynomial Multiplication   2017-12-19 \n"\
                   "1  Design of Computer Programs 2017-10-20 \n"
        self.assertEqual(output, expected)
    
    def test_display_todays_stuff(self):
        out = StringIO()
        with contextlib.redirect_stdout(out):
            display_todays_stuff(self.cur)
        output = out.getvalue()
        self.assertTrue(len(output) > 0)


if __name__ == '__main__':
    unittest.main()
