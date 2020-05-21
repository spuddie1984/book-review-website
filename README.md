## Book Review Website Flask based App
_This project is one of the projects on cs50w track_ [check it out here](https://docs.cs50.net/web/2019/x/projects/1/project1.html)

## About My App

**I've used a library to use an .env file....just create your own with the required env variables (like api key and database url)**


### File Structure

I've tried to break the views/templates up into different directories so that it is easier to navigate
```

--templates
    |--books
    |   |---index.html
    |   |---results.html
    |   |---show.html
    |
    |--comments
    |   |---new.html
    |
    |--users
    |   |---login.html
    |   |---register.html
    |
    |--base_template.html
    |--error.html
    |--landing.html
```
The rest of the structure is self explanatory.

### Routing

Added Custom Error handlers (404 and 500)

**Routing Table**

|         Name         |          URL         | Verb |                        Description                         |
|----------------------|----------------------|------|------------------------------------------------------------|
|Register              |    /register         | GET  | Display a registration form                                |
|Create a New User     |    /register         | POST | Create a new user in the DB and redirect to search page    |
|Login                 |    /login            | GET  | Display login form                                         |
|Login Submission      |    /login            | POST | Authenticate user in DB then redirect to search page       |
|Logout                |    /logout           | GET  | Logout User redirect to landing page                       |
|Search/Index          |    /books            | GET  | display a search form                                      |
|Display Search Results|    /books            | POST | Search the DB show the Results                             |
|Individual Book       |  /books/:id          | GET  | Display details of Individual Book                         |
|New Comment           |/books/:id/comment/new| GET  | Display a form to add a new comment                        |
|Create New Comment    |  /books:id/comment   | POST | Add new comment to DB then redirect to individual book page|
|Api Access            |  /api/:isbn          | GET  | Search DB for isbn return book details or 404 error        |


### Extras (things added outside the requirement, for cs50w project 1)

- Mobile responsive with bootstrap
- Custom override styles to add a personal touch
- free for commercial use logos to make the app look more professional
- flash messages (needs a bit of tweaking) to register/login, book, individual book and comment routes
- Extra api request from goodreads.  Use beautiful soup to parse xml encoded api data from goodreads then show (on an individual book page) the extra data (book image and book description)
- Hash passwords stored in the DB with bcrypt
- Use dotenv so that env variables can be stored in one spot, namely the .env file

#### 1st Commit - Routing, Basic Setup

- Add all Routes Login/out, Register, books index/search, comments (full crud functionality), individual book page, api and 404 catch all route
- setup base template in jinja2 
- integrate bootstrap 4
- Basic Navbar
- setup static files directory
- add env variables to .env file (api key, database details etc...)
- add requirements file
- add books in books.csv to database with import.py file

#### 2nd Commit - Hookup db to Register and Login routes, Hookup Templates

- Add App Notes folder for personal notes 
- Add a Users Table and Comments table to our database 
- Add images to static img directory (background images, icons)
- styling updates - add more features to base template....icons, color scheme, footer etc
- add login/register form to landing page
- Update template file structure
- Add books  /index and /show templates - add forms to these templates as well
- Add users  /login and /register templates - add forms to these templates as well
- Add database functionality to register and login routes

#### 3rd Commit - Add Sessions Hookup books db routes

- Add sessions and add logic to all routes that require user authentication including redirect functionality
- Hook up DB search functionality to index/search books route.  Can search using part of either the title,
author or isbn.
- show a list of search results that a user can click to go to the individual books details page
- setup individual show book route...show the title author isbn
- add a button to show book route so the user can leave a comment
- hookup api good reads to show book route...show review count and average rating
- update/fix static image links to use url_for method

#### 4th Commit - Comment DB integration

- Add form to new comment route with ability to add a comment and rating (one comment/rating per book per user)
- Add new comment to DB with user id and and comment id to associated book in the DB as well
- store username and user_id in session
- improve redirects on login route
- Add logic to show template for comments (if have messages show them else display a message "no comments")
- Add logic to prevent user from leaving more then one comment per book
- Add user dictionary with username and user_id (from DB)
- Add book title to tab bar in SHOW book template

#### 5th Commit - Styling Updates, Flash Messages

- Fix mobile responsiveness
- Fix footer overlap
- style search results box
- convert users rating to a star rating (at the moment its just a number)
- Update forms with required on neccessary inputs
- Add flash messages

#### 6th Commit - Hash passwords, add more details from goodreads api to show page, 404 page

- Install and use the B-crypt hashing library
- refactor register/login routes, store hashed password in DB
- setup 404 error handler route and style accordingly
- Use Beautiful Soup to parse xml pages
- Add goodreads book data (extracted using beautiful soup) to show book page
- Refactor api route so that a json response is returned if somebody submits a get request

#### 7th Commit - General Tidy-Up 

- remove flash message comments 
- Add routes table to readme
- style updates

#### 8th Commit - Improve Login UX for Demo Purposes

- Add detials on landing page about how to login
- prefill login form with username and password so that people can test the App's functionality
