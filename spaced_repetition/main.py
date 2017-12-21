#!/usr/bin/env python3
"""Main script for the spaced repitition app."""
from urllib import parse

from spaced_repetition import database
from spaced_repetition import functions
from spaced_repetition.env import DATABASE_URL

def main():
    """Main function of the app."""
    url = parse.urlparse(DATABASE_URL)
    conn = database.db_connect(url)
    cur = conn.cursor()

    functions.display_todays_stuff(cur)

if __name__ == "__main__":
    main()