import os
import requests
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


if not os.getenv("LOCAL_DATABASE_URL"):
    raise RuntimeError("LOCAL_DATABASE_URL is not set")

engine = create_engine(os.getenv('LOCAL_DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))

# create table schema for books Schema: 
#     Table Name: "bookslist"
#     id SERIAL primary key (auto incrementing integer)
#     isbn: VARCHAR (string)  some isbn numbers contain characters
#     title: VARCHAR (string)
#     author: VARCHAR (string)
#     year: INTEGER
db.execute('CREATE TABLE IF NOT EXISTS "bookslist" ('
               'id SERIAL primary key,'
               'isbn VARCHAR,'
               'title VARCHAR,'
               'author VARCHAR,'
               'year INTEGER'');')
db.commit()

# setup csv reader to read the books.csv file
with open('books.csv') as books_file:
    # delimiter="," seperates each column entry 
    # quotechar='"' delimiter , character is ignored in  quoted strings 
    bookreader = csv.reader(books_file, delimiter=',', quotechar='"')
    
    # skip the first line that contains the header row
    next(bookreader)
    
    # loop through each book entry and write to the database
    for isbn, title, author, year in bookreader:
        
        # used to check if books have been entered correctly
        print(f"ISBN:{isbn} Title:{title} Author:{author} Year:{year}")
        
        db.execute("INSERT INTO bookslist (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                  {'isbn': isbn, 'title': title, 'author': author, 'year': year})
        db.commit()
db.close()