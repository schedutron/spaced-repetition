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
    for i, column in enumerate(header):
        length = max(max([len(str(row[i])) for row in rows]), len(column))
        lengths.append(length)
        string = '%-' + str(length) + 's'
        print(string % column, end=' ')
    print('\n')
    for row in rows:
        for i in range(len(header)):
            string = '%-' + str(lengths[i]) + 's'
            print(string % row[i], end=' ')
        print()


def display_todays_stuff(cur):
    """Display stuff to learn today."""
    learn_ids = learn_today(cur)
    cur = database.get_rows_for_ids(cur, learn_ids)
    display_rows(cur)


def insert_source(cur):
    """Take input from user and add to notebooks relation."""
    print("Press enter to skip optional entries.\n")
    title = ''
    while not title:
        title = input("Enter title: ")
    while True:
        begin_date = input("Enter date as dd/mm/yyyy (optional): ")
        if not begin_date:
            break
        try:
            begin_date = datetime.datetime.strptime(begin_date, '%d-%m-%Y')
            break
        except ValueError:
            print("Please enter a valid input.")
    if not begin_date:
        begin_date = None
    database.insert_row(cur, 'notebooks', '(title, begin_date, total_entries)',
                        (title, begin_date, 0)
                       )
    print("\nSource added successfully!")


def insert_entry(cur):
    """Take input from user and add to to_learn relation."""
    print("Press enter to skip optional fields.\n")
    err_msg = "Please enter a valid input."
    title = ''
    while not title:
        title = input("Enter title: ")
    while True:
        page_num_start = input("Enter start page (optional): ")
        if not page_num_start:
            break
        try:
            page_num_start = int(page_num_start)
            break
        except ValueError:
            print(err_msg)
    if not page_num_start:
        page_num_start = None
    
    while True:
        page_num_end = input("Enter end page (optional): ")
        if not page_num_end:
            break
        try:
            page_num_end = int(page_num_end)
            break
        except ValueError:
            print(err_msg)
    if not page_num_end:
        page_num_end = None
    
    while True:
        add_date = input(
            "Enter add_date as dd-mm-yyyy (skip to use today's date): ")
        if not add_date:
            break
        try:
            add_date = datetime.datetime.strptime(add_date, 
                                                       '%d-%m-%Y')
            break
        except ValueError:
            print(err_msg)
    
    if not add_date:
        add_date = datetime.datetime.now().date()
    
    while True:
        last_revision = input("Enter last revision date as dd-mm-yyyy (skip "
                              "to use today's date): ")
        if not last_revision:
            break
        try:
            last_revision = datetime.datetime.strptime(last_revision, '%d-%m-%Y')
            break
        except ValueError:
            print(err_msg)
    
    if not last_revision:
        last_revision = datetime.datetime.now().date()

    source_title = input("Enter source title (optional): ")
    notebook_id = database.get_source_id_by_title(cur, source_title)
    if not notebook_id and source_title:
        print("No such source found. Please add it separately.")
        return
    input_tuple = (title, page_num_start, page_num_end, add_date, last_revision, notebook_id, 1)
    database.insert_row(cur, 'to_learn',
                        '(title, page_num_start, page_num_end, add_date, '
                        'last_revision, notebook_id, level)', input_tuple)
    print("\nEntry added successfully!")
