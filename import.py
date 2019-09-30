import os
import requests
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

print(os.getenv('DATABASE_URL'))

if not os.getenv("LOCAL_DATABASE_URL"):
    raise RuntimeError("LOCAL_DATABASE_URL is not set")

engine = create_engine(os.getenv('LOCAL_DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))

# create table for books Schema: 
#   Table Name: "bookslist"
#   id SERIAL primary key (auto incrementing integer)
#   isbn: VARCHAR (string)  some isbn numbers contain characters
#   title: VARCHAR (string)
#   author: VARCHAR (string)
#   year: INTEGER
#   comments_id INTEGER REFERENCES comments
db.execute('CREATE TABLE IF NOT EXISTS "bookslist" ('
            'id SERIAL primary key,'
            'isbn VARCHAR,'
            'title VARCHAR,'
            'author VARCHAR,'
            'year INTEGER'');')
db.commit()

# Create table for Users Schema:
#   Table Name: "users"
#   username: VARCHAR (string) primary key NOT NULL (must have an entry)
#   password: VARCHAR NOT NULL (hashed password)
db.execute('CREATE TABLE IF NOT EXISTS "users" ('
            'id SERIAL PRIMARY KEY,'
            'name VARCHAR NOT NULL,'
            'username VARCHAR NOT NULL,'
            'password VARCHAR NOT NULL'');')
db.commit()

# Create table for Comments Schema:
#   Table Name: "comments"
#   comment_id: SERIAL primary key 
#   comment: VARCHAR 
#   user_rating: INTEGER NOT NULL
#   user_id: INTEGER REFERENCES users(user_id)
db.execute('CREATE TABLE IF NOT EXISTS "comments"('
            'comment_id SERIAL PRIMARY KEY,'
            'comment VARCHAR,'
            'user_rating INTEGER NOT NULL,'
            'book_id INTEGER REFERENCES bookslist(id),'
            'user_id INTEGER REFERENCES users(id)'');')
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
        if db.execute('SELECT * FROM bookslist;').rowcount != 5000:
            db.execute("INSERT INTO bookslist (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {'isbn': isbn, 'title': title, 'author': author, 'year': year})
            db.commit()
        else:
            raise Exception("Error, sorry those books already exist in this table")
db.close()