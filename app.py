import os
import requests

from flask import Flask, session
from flask import render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
# so we can use a .env file to store our environment variables
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
    return render_template('base_template.html')

# Register Route   
@app.route("/register", methods=['GET','POST'])
def register():
    return render_template('base_template.html')

# Login Route
@app.route("/login", methods=['GET','POST'])
def login():
    return render_template('base_template.html')

# Logout Route
@app.route("/logout", methods=['GET'])
def logout():
    return render_template('base_template.html')

# Books INDEX/SEARCH Route
@app.route("/books", methods=['GET','POST'])
def books():
    return render_template('base_template.html')

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