#!/usr/bin/env python3
"""Main script for the spaced repitition app."""
# Add a boolean 'saturated' column to specify whether the entry is in
# saturated mode, when the initial level is > 1. This is to be used for
# uniform work distribution so that there isn't too much load at any given
# day.
from urllib import parse

from spaced_repetition import database
from spaced_repetition import functions
from spaced_repetition.env import DATABASE_URL

def main():
    """Main function of the app."""
    url = parse.urlparse(DATABASE_URL)
    conn = database.db_connect(url)
    cur = conn.cursor()
    while True:
        query = input("-|-> ")
        if query.lower() == "today":
            functions.display_todays_stuff(cur)
        elif query.lower() == "display all":
            functions.display_all_entries(cur)
        elif query.lower() == "update":
            ids = input("Enter the ids that you have revised: ")
            ids = [int(i.strip()) for i in ids.split(',')]
            database.set_for_next_date(cur, ids)
            print("Update Done:\n")
            cur = database.get_rows_for_ids(cur, ids)
            functions.display_rows(cur)
        elif query.lower() == "insert entry":
            functions.insert_entry(cur)
        elif query.lower() == "insert source":
            functions.insert_source(cur)
        elif query.lower() == "exit":
            print("Goodbye.")
            break
        elif query:  # Skip this when the user just presses Enter.
            print("Please enter a valid query.")


if __name__ == "__main__":
    main()
