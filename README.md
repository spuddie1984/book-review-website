## Book Review Website Flask based App
_This project is one of the projects on cs50w track_ [check it out here](https://docs.cs50.net/web/2019/x/projects/1/project1.html)



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