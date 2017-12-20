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
        if get_next_date(record[1], record[2]) <= today:
            to_learn.append(record[0])
    return to_learn


def get_colnames(cur):
    """Get's column names for a given query. It's assumed that the cursor is
    passed after an execute*() call."""
    return [desc[0] for desc in cur.description]


def display_rows(cur):
    """Displays the rows in a nice tabular form."""
    header = get_colnames(cur)
    rows = cur.fetchall()
    lengths = []  # Contains length of largest word in the column at the same index.
    for i in range(len(header)):
        length = max(max([len(str(row[i])) for row in rows]), len(header[i]))
        lengths.append(length)
        string = '%-' + str(length) + 's'
        print(string % header[i], end=' ')
    print('\n')
    for row in rows:
        for i in range(len(header)):
            string = '%-' + str(lengths[i]) + 's'
            print(string % row[i], end=' ')
        print()


def display_todays_stuff(cur):
    """Display stuff to learn today."""
    import sys
    learn_ids = learn_today(cur)
    cur = database.get_rows_for_ids(cur, learn_ids)
    display_rows(cur)
