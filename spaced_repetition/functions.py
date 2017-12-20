"""Utility functions for use elsewhere in the package"""
import datetime
from spaced_repetition import database

def get_next_date(last_revision, level):
    """Calculates date for next revision based on previous revision date and
    current level."""
    return last_revision + datetime.timedelta(days=level)


def learn_today(cur):
    """Retrieve id's of items to learn today."""
    cur = database.get_last_rev_with_id_and_level(cur)
    today = datetime.datetime.now().date()
    to_learn = []
    for record in cur:
        if get_next_date(record[1], record[2]) == today:
            to_learn.append(record[0])
    return to_learn
