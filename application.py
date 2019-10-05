import os
import requests

from flask import Flask, flash, session, request, escape, redirect, url_for
from flask import render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
# for parsing xml data from the goodreads book api
from bs4 import BeautifulSoup

# env file
load_dotenv()

app = Flask(__name__)

bcrypt = Bcrypt(app)

# Check for environment variable
# swap between LOCAL_DATABASE_URL AND LIVE_DATABASE_URL for production and development environments
if not os.getenv("LOCAL_DATABASE_URL"):
    raise RuntimeError("LOCAL_DATABASE_URL is not set")


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
# Change database when pushed to a live server
# swap between LOCAL_DATABASE_URL AND LIVE_DATABASE_URL for production and development environments
engine = create_engine(os.getenv("LOCAL_DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


# landing page route
@app.route("/", methods=['GET'])
def index():
    return render_template('landing.html')

# Register Route   
# Register route disabled the app will be used for demo purposes only
@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == "GET":
        return render_template('/users/register.html')
    elif request.method == "POST":
        # grab the form data escape all data (sanitize) hash the password then enter the data into the database
        user_data = {
            "name": escape(request.form['name']),
            "username": escape(request.form['username']),
            "password": bcrypt.generate_password_hash(escape(request.form['password'])).decode('utf-8'),
        }
        # Insert user info into DB (Name, username, password(will be hashed))
        if db.execute('SELECT username FROM users WHERE username = :username',{'username':user_data['username']}).rowcount == 0:
            db.execute("INSERT INTO users (name, username, password) VALUES (:name, :username, :password)",
            {'name':user_data['name'], 'username':user_data['username'], 'password':user_data['password']})
            # grab user data from database will use DB user id in sessions['username] 
            db_user_data = db.execute('SELECT * FROM users WHERE username = :username',{'username':user_data['username']}).fetchall()
            db.commit()
            # initial session variable then write user to the 'username variable
            session['username'] = None
            session['username'] = {'username':db_user_data[0].username, 'id':db_user_data[0].id}
            flash(u'Successfully Logged In', 'success')
            return redirect(url_for('books'))
        else:
            flash(u'Sorry that user already exists', 'error')
            return redirect(url_for('register'))
        
# Login Route
@app.route("/login", methods=['GET','POST'])
def login():
    if session.get('username') is None:
        if request.method == "GET":
            return render_template('/users/login.html')
        elif request.method == "POST":
            # grab sanatized user data from the form check if user exists in the database
            username = escape(request.form['username'])
            password = request.form['password']
            if db.execute('SELECT * FROM users WHERE username = :username',{'username':username}).rowcount == 0:
                flash(u'That user doesn\'t exist, please register or try again', 'error')
                return redirect(url_for('index'))
            else:
                # check user entered correct password if not redirect to login again
                db_user_data = db.execute('SELECT * FROM users WHERE username = :username',{'username':username}).fetchall()
                if db_user_data[0].username == username and bcrypt.check_password_hash(db_user_data[0].password, password):
                    session['username'] = {'username':db_user_data[0].username, 'id':db_user_data[0].id} # consider refactoring to use user_id from DB
                    flash(u'Successfully Logged In', 'success')
                    return redirect(url_for('books'))
                else:
                    flash(u'Try logging In again', 'error')
                    return redirect(url_for('login'))
    else:
        return redirect(url_for('books'))

# Logout Route
@app.route("/logout", methods=['GET'])
def logout():
    session['username'] = None
    flash(u'Successfully Logged Out', 'success')
    return redirect(url_for('index'))

# Books INDEX/SEARCH Route
@app.route("/books", methods=['GET','POST'])
def books():
    if session['username'] is None:
        flash(u'You need to login for that !!!', 'error')
        return redirect(url_for('index'))
    else:
        if request.method == "GET":
            return render_template('/books/index.html')
        elif request.method == "POST":
            search_request = request.form['search']
            # search the DB for a partial or full match from columns for books ISBN,AUTHOR or TITLE
            results = db.execute('SELECT * FROM bookslist WHERE isbn ~* :search_request OR title ~* :search_request OR author ~* :search_request', {'search_request':search_request}).fetchall()
            print(results)
            db.commit()
            if len(results) != 0:
                return render_template('/books/results.html', results=results)
            else:
                flash(u'Sorry no books matched your search, please try again!!', 'error')
                return redirect(url_for('books'))

# Individual Books SHOW Route
@app.route("/books/<id>", methods=['GET'])
def show_book(id):
    if session['username'] is None:
        flash(u'You need to login for that !!!', 'error')
        return redirect(url_for('index'))
    else:
        # get the Individual book from DB via the id passed into show_book route 
        session_user = session.get('username')
        book = db.execute('SELECT * FROM bookslist LEFT JOIN comments ON comments.book_id = :book_id WHERE bookslist.id = :book_id',{'book_id':id}).fetchall()
        # Api calls to goodreads
        # review count api call
        good_reads_reviews = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": os.getenv('API_KEY'), "isbns": book[0].isbn}).json()
        # full book data api call (xml format only)
        good_reads_book_data = requests.get("https://www.goodreads.com/book/isbn/", params={"isbn": book[0].isbn, "key": os.getenv('API_KEY')})
        # extract book data using Beautiful soup
        data_soup = BeautifulSoup(good_reads_book_data.content, 'xml')
        # push this to the show template  
        extracted_book_data = {
            "description": data_soup.find('description').get_text(),
            "image": data_soup.find('image_url').get_text()
        }
        print(extracted_book_data)
        return render_template('/books/show.html', 
            book=book, extracted_book_data=extracted_book_data,
            good_reads_reviews=good_reads_reviews, 
            session_user_id=session_user['id']
        )
        
# NEW Comment Route
@app.route("/books/<id>/comment/new", methods=['GET'])
def new_comment(id):
    # display new comment form if user is logged in
    if session['username'] is None:
        flash(u'You need to login for that !!!')
        return redirect(url_for('index'))
    else:
        return render_template('/comments/new.html', id=id)

# CREATE New Comment Route
@app.route("/books/<id>/comment", methods=['POST'])
def create_comment(id):
    # if user is loggedIn save (espaced)comment data to DB then redirect to show page
    if session['username'] is None:
        flash(u'You need to login for that !!!', 'error')
        return redirect(url_for('index'))
    else:
        user = session.get('username')
        # Check DB if user has commented on this book already if so send flash message 'sorry you have already commented on this book'
        if db.execute('SELECT book_id, user_id FROM comments WHERE book_id = :book_id AND user_id = :user_id',{'book_id':id, 'user_id':user['id']}).rowcount == 0:
            # Save newly created comment to DB in comments table and associate with the books and users table
            # insert into comments then assocaite users and comments table
            comment = escape(request.form['comment'])
            rating = escape(request.form['star-rating'])
            save_comment = db.execute('INSERT INTO comments (comment, user_rating, book_id, user_id) VALUES (:comment, :user_rating, :book_id, :user_id)',{"comment":comment, "user_rating": rating, "book_id": id, "user_id": user["id"] })
            db.commit()
            flash(u"You've successfully added a comment", 'success')
            return redirect(url_for('show_book', id=id))
        else: 
            flash(u"Sorry you've already added a comment, 1 comment per user/book", 'error')
            return redirect(url_for('show_book', id=id))
    
# Api Route 
@app.route("/api/<isbn>", methods=['GET'])
def api(isbn):
    response = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": os.getenv("API_KEY"), "isbns": isbn})
    if response.status_code == 200:
        if db.execute('SELECT isbn FROM bookslist WHERE isbn = :isbn', {'isbn': isbn}).rowcount != 0:
            find_book_data = db.execute('SELECT title, author, year, isbn FROM bookslist WHERE isbn = :isbn', {'isbn': isbn}).fetchall()
            # convert the get request response to a json like dictionary
            book_reviews = response.json()
            # return a json object
            return {
                "title": find_book_data[0].title,
                "author": find_book_data[0].author,
                "year": find_book_data[0].year,
                "isbn": find_book_data[0].isbn,
                "review_count": book_reviews['books'][0]['reviews_count'],
                "average_score": book_reviews['books'][0]['average_rating']
            }
    else:
        # 404 error response
        return {'error': '404  That book doesn\'t exist in our database'}


# 404/Catch all Route 
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error=e)

# 500 Server error handler
@app.errorhandler(500)
def server_problem(e):
    return render_template('error.html', error=e)