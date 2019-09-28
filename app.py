import os
import requests

from flask import Flask, session, request, escape, redirect, url_for
from flask import render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Check for environment variable
if not os.getenv("LOCAL_DATABASE_URL"):
    raise RuntimeError("LOCAL_DATABASE_URL is not set")


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
# Change database when pushed to a live server
engine = create_engine(os.getenv("LOCAL_DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# landing page route
@app.route("/", methods=['GET'])
def index():
    session.get('username', None)
    return render_template('landing.html')

# Register Route   
@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == "GET":
        return render_template('/users/register.html')
    elif request.method == "POST":
        # grab the form data escape all data (sanitize) then enter the data into the database
        user_data = {
            "name": escape(request.form['name']),
            "username": escape(request.form['username']),
            "password": escape(request.form['password']),
        }
        # Insert user info into DB (Name, username, password(will be hashed))
        if db.execute('SELECT username FROM users WHERE username = :username',{'username':user_data['username']}).rowcount == 0:
            db.execute("INSERT INTO users (name, username, password) VALUES (:name, :username, :password)",
            {'name':user_data['name'], 'username':user_data['username'], 'password':user_data['password']})
            db.commit()
            session['username'] = user_data.username # Consider refactoring to use user_id in the DB
            return redirect(url_for('books')) # add flash message "Succesfully logged In"
        else:
            return redirect(url_for('register')) # add flash message "Sorry that user already exists"
        
# Login Route
@app.route("/login", methods=['GET','POST'])
def login():
    if session.get('username') is None:
        if request.method == "GET":
            return render_template('/users/login.html')
        elif request.method == "POST":
            # grab sanatized user data from the form check if user exists in the database
            username = escape(request.form['username'])
            password = escape(request.form['password'])
            if db.execute('SELECT * FROM users WHERE username = :username',{'username':username}).rowcount == 0:
                return redirect(url_for('login')) # add flash message "sorry that user doesn't exist please register or try again"
            else:
                # check user entered correct password if not redirect to login again
                db_user_data = db.execute('SELECT * FROM users WHERE username = :username',{'username':username}).fetchall()
                if db_user_data[0].username == username and db_user_data[0].password == password:
                    session['username'] = username # consider refactoring to use user_id from DB
                    return redirect(url_for('books')) # add flash message "Successfully logged In"
                else:
                    return redirect(url_for('login')) # add flash message "sorry wrong username or password"
    else:
        return redirect(url_for('books')) # add flash message You're already logged in

# Logout Route
@app.route("/logout", methods=['GET'])
def logout():
    session['username'] = None
    return redirect(url_for('index'))

# Books INDEX/SEARCH Route
@app.route("/books", methods=['GET','POST'])
def books():
    if session['username'] is None:
        return redirect(url_for('index')) # add flash message "You need to login for that !!!"
    else:
        if request.method == "GET":
            return render_template('/books/index.html')
        elif request.method == "POST":
            search_request = request.form['search']
            # search the DB for a partial or full match from columns for books ISBN,AUTHOR or TITLE
            results = db.execute('SELECT * FROM bookslist WHERE isbn ~* :search_request OR title ~* :search_request OR author ~* :search_request', {'search_request':search_request}).fetchall()
            db.commit()
            if len(results) != 0:
                return render_template('/books/results.html', results=results)
            else:
                return redirect(url_for('books')) # add flash message "sorry no books matched your search, please try again"

# Individual Books SHOW Route
@app.route("/books/<id>", methods=['GET'])
def show_book(id):
    if session['username'] is None:
        return redirect(url_for('index')) # add flash message "You need to login for that !!!"
    else:
        # get the Individual book from DB via the id passed into show_book route 
        book = db.execute('SELECT * FROM bookslist WHERE book_id = :id',{"id":id}).fetchall()
        print(book)
        good_reads_data = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": os.getenv('API_KEY'), "isbns": book[0].isbn}).json()
        return render_template('/books/show.html', book=book, good_reads_data=good_reads_data)
        

# New Comment Route
@app.route("/books/<id>/comment/new", methods=['POST'])
def new_comment(id):
    if session['username'] is None:
        return redirect(url_for('index')) # add flash message "You need to login for that !!!"
    else:
        return render_template('/comments/new.html')

# Create New Comment Route
@app.route("/books/<id>/comment", methods=['POST'])
def create_comment():
    if session['username'] is None:
        return redirect(url_for('index')) # add flash message "You need to login for that !!!"
    else:
        return render_template('base_template.html')

# Edit Comment Route
@app.route("/books/<id>/comment/<comment_id>/edit", methods=['GET'])
def edit_comment():
    if session['username'] is None:
        return redirect(url_for('index')) # add flash message "You need to login for that !!!"
    else:
        return render_template('base_template.html')

# Update and Destroy Comment Route
@app.route("/books/<id>/comment", methods=['PUT','DELETE'])
def comment():
    if session['username'] is None:
        return redirect(url_for('index')) # add flash message "You need to login for that !!!"
    else:
        return render_template('base_template.html')
    
# Api Route 
@app.route("/books/api/<isbn>", methods=['GET'])
def api(isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "API_KEY", "isbns": isbn})
    if res.status_code == 200:
        return "Well done"
    else:
        return 'Sorry we encounted a problem. This is the Error Code !!!!'

# 404/Catch all Route 
@app.route("/books/<catch_all>", methods=['GET'])
def catch_all():
    return render_template('base_template.html')