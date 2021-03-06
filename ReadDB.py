# ReadDB v 0.0.2
# Francis Windram 2016
# Python 3.4
#
# Created:  21/12/16
# Modified: 22/12/16
#
# A Python3/SQL project for building and maintaining a book database.
#
# ===== TO DO LIST =====
# TODO - If extant, open SQLite db
# DONE - Else construct new DB on first run with required tables/columns
# TODO - ADD basic SQL logic for addition & deletion
# TODO - ADD SQL search functionality
# Done - ADD auto-ISBN lookup for quick entry (using isbntools)
#       - isbnlib.meta() returns dict in the following style:
#     {
#         'Year':'yyyy',
#         'ISBN-13':'xxxxxxxxxxxxx',
#         'Publisher':'publisher',
#         'Authors':['Fore M. Sur', 'First Last'],
#         'Title':'The Title of the Book'
#         'Language':'language'
#     }
# TODO - ADD isbn_lookup error handling
# TODO - ADD csv import function
# TODO - ADD error logging
# TODO - ADD tkinter interface


import sqlite3
import isbnlib


class Book:

    bookid = "NULL"

    def __init__(self, year, isbn13, publisher, author_fname, author_sname, title, language):
        self.year = year
        self.isbn13 = isbn13
        self.publisher = publisher
        self.author_fname = author_fname
        self.author_sname = author_sname
        self.title = title
        self.language = language


def create_db(recreate=False):
    """Creates DB with correct tables (drops table if required)"""
    connection = sqlite3.connect("books.sqlite")
    cursor = connection.cursor()
    if recreate:
        try:
            print("Dropping table...")
            cursor.execute("""DROP TABLE employee;""")
            print("Table dropped.")
        except sqlite3.OperationalError:
            print("\n!!! === No table present === !!!\n")
    dbcreate_cmd = """
    CREATE TABLE books (
    bookid INTEGER PRIMARY KEY,
    title VARCHAR(255),
    surname VARCHAR(30),
    forename VARCHAR(30),
    isbn INTEGER(13),
    publisher VARCHAR(100),
    year INTEGER,
    language VARCHAR(30));"""
    print("Creating table...")
    cursor.execute(dbcreate_cmd)
    print("Table created.")

    connection.commit()
    connection.close()


def isbn_lookup(isbn):
    """Looks up ISBN and spits out object with all necessary data for DB"""
    # b_meta test data
    b_meta = {'Year': '2015',
              'ISBN-13': '9780230769465',
              'Publisher': '',
              'Authors': ['Peter F. Hamilton', 'Piper-Verlag', 'Wolfgang Thon'],
              'Title': 'The abyss beyond dreams: a novel of the Commonwealth',
              'Language': ''
              }
    primary_author = ['']
    if isbnlib.is_isbn13(isbn):     # if ISBN provided is ISBN-13
        isbn = isbnlib.EAN13(isbn)  # convert to validated, canonical ISBN-13 (remove hyphens etc.)
        b_meta = isbnlib.meta(isbn)          # look up metadata, return dict
        primary_author = b_meta["Authors"][0].split(" ")

    book_inst = Book(
        b_meta["Year"],
        b_meta["ISBN-13"],
        b_meta["Publisher"],
        primary_author[0],
        primary_author[len(primary_author) - 1],
        b_meta["Title"],
        b_meta["Language"],
    )

    return book_inst
