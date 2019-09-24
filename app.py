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
    return render_template('landing.html')

# Register Route   
@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == "GET":
        return render_template('/users/register.html')
    elif request.method == "POST":
        # grab the form data escape all data (sanitize) then enter the data into the database
        userData = {
            "name": escape(request.form['name']),
            "username": escape(request.form['username']),
            "password": escape(request.form['password']),
        }
        if db.execute('SELECT username FROM users WHERE username = :username',{'username':userData['username']}).rowcount == 0:
            db.execute("INSERT INTO users (name, username, password) VALUES (:name, :username, :password)",
            {'name':userData['name'], 'username':userData['username'], 'password':userData['password']})
            db.commit()
            return render_template('/books/index.html', userData=userData['username']) # add flash message "Succesfully logged In"
        else:
            return redirect(url_for('register')) # add flash message "Sorry that user already exists"
        
# Login Route
@app.route("/login", methods=['GET','POST'])
def login():
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
            dbUserData = db.execute('SELECT * FROM users WHERE username = :username',{'username':username}).fetchall()
            if dbUserData[0].username == username and dbUserData[0].password == password:
                return render_template('/books/index.html') # add flash message "Successfully logged In"
            else:
                return redirect(url_for('login')) # add flash message "sorry wrong username or password"

# Logout Route
@app.route("/logout", methods=['GET'])
def logout():
    return render_template('base_template.html')

# Books INDEX/SEARCH Route
@app.route("/books", methods=['GET','POST'])
def books():
    if request.method == "GET":
        return render_template('/books/index.html')
    elif request.method == "POST":
        return render_template('/books/index.html')

# Individual Books SHOW Route
@app.route("/books/<id>", methods=['GET'])
def show_book():
    return render_template('base_template.html')

# New Comment Route
@app.route("/books/<id>/comment/new", methods=['POST'])
def new_comment():
    return render_template('base_template.html')

# Create New Comment Route
@app.route("/books/<id>/comment", methods=['POST'])
def create_comment():
    return render_template('base_template.html')

# Edit Comment Route
@app.route("/books/<id>/comment/<comment_id>/edit", methods=['GET'])
def edit_comment():
    return render_template('base_template.html')

# Update and Destroy Comment Route
@app.route("/books/<id>/comment", methods=['PUT','DELETE'])
def comment():
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