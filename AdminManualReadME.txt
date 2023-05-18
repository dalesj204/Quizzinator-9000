+++++++++++++++++++++++++++++++++++++++++++++++++
Admin Manual
+++++++++++++++++++++++++++++++++++++++++++++++++
Welcome to the Quizzinator 9000 Administration Guide!
+++++++++++++++++++++++++++++++++++++++++++++++++
Creators:
Shawn Cai, Jordan Dales, Hayden Dustin, Jacob Fielder, 
Evan Klindt, Hannah Pinard, and Nathan Prelewicz
+++++++++++++++++++++++++++++++++++++++++++++++++
Table of Contents:
  -Server Start-Up
  -Script Info
  -Sign in
  -Password Resets
  -Information Editing
  -Teacher Admin Guide
  -Source Code Guide
+++++++++++++++++++++++++++++++++++++++++++++++++
Server Start-Up
+++++++++++++++++++++++++++++++++++++++++++++++++
To initialize the server, run: 
[python varient] manage.py clean
docker-compose -f local.yml build
docker-compose -f local.yml up

And thats it!
The python/docker scripts will take care of the rest.
To view the website, go to '127.0.0.1:8000'

To see/edit python scrips go to:
 ../quizzes/management/commands

To see/edit docker scripts go to:
 ../compose/local/django and view the start script

To Remove demo data go to the docker start script and comment out the line:
 'python manage.py loaddata quiz_app_fixtures.json'

This will leave you with a clean database to work from.
+++++++++++++++++++++++++++++++++++++++++++++++++
Script Info
+++++++++++++++++++++++++++++++++++++++++++++++++
Clean:
  -Clean clears all database entries
  -DO NOT CLEAN ON A DATABASE IN USE (effectively drops all tables)

Build:
  -Builds program locally
  -runs tests
  -redundant

Docker Build: 
  -Docker command that initializes a container
  -Checks .yml files for errors
  -Builds based on instruction in .yml file and SETTINGS file.

Docker Up:
  -Spins up container
  -One last check for errors
  -Listens on 0.0.0.0:8000

Start:
  -File that contains intstruction for Docker up command.
  -Any command in the start script will be run upon spin up
+++++++++++++++++++++++++++++++++++++++++++++++++
Sign In
+++++++++++++++++++++++++++++++++++++++++++++++++
  -New admin setup command: django-admin createsuperuser, follow instruction
  -Remember your username and password
 Defaults:
  -Default test admin on local: user = admin, pass = test
  -Default test teacher: user = grabowski@gmail.com, pass = test
  -Default test students: user = richieman@gmail.com, pass = test
  -Default test user = rosiewoman@gmail.com, pass = test
  -Default test user = hailey@gmail.com, pass = test
+++++++++++++++++++++++++++++++++++++++++++++++++
Password Resets
+++++++++++++++++++++++++++++++++++++++++++++++++
  -Click on users
  -Students
  -Password
  -Change Password
  -Tell them their new temporary password
+++++++++++++++++++++++++++++++++++++++++++++++++
Information Editing
+++++++++++++++++++++++++++++++++++++++++++++++++
  -Adding a User:
	- Click users
	- Add new user
	- Fill required information
  -Adding a Question
	- click questions
	- add question
	- fill information
  -Adding a Quiz
	- click quiz
	- add quiz
	- select desired questions
	- select desired tags
  -Removing Information
	- Click desired table
	- select entry to remove
	- click delete 
+++++++++++++++++++++++++++++++++++++++++++++++++
Teacher Admin Guide
+++++++++++++++++++++++++++++++++++++++++++++++++
User Privilege:
  -All Teachers are considered admins, although they do not have access to the admin page.
  Password Resets:
	All Teachers may reset any users password from their homepage
	All Teachers may register a new teacher from their homepage
	All users may reset their own password from their homepage
+++++++++++++++++++++++++++++++++++++++++++++++++
Source Code Guide
+++++++++++++++++++++++++++++++++++++++++++++++++
Models
  - All Models are given fields which relate to the columns of data and their types as they will appear in the database
  - These should not be edited unless you must add new tables to the database.
	
  Models with Admin Function:
    -Class
    -Quiz
    -Tag
    -Question
    -Options
    -Teacher
    -Student
    -User
+++++++++++++++++++++++++++++++++++++++++++++++++
Views
  - Views are the logic of the pages
  - Each view and their functionality are explained in the comment block above them
  - These can be edited if new functionality is to be added to the web pages.
+++++++++++++++++++++++++++++++++++++++++++++++++
Templates
  - Templates are the HTML of the webpages
  - Django allows for some logic within the HTML
  - Base_Generic is our main HTML code that is inherited by all other HTML files
	- Base_Generic contains the universal parts of all pages such as the nav-bar
  - index is our base home page, it contains the welcome block as well as homepage options like 'Create/Take Quiz'
  - All HTML files past this are named for their function. If you must edit say, Take a quiz, the HTML is named 'take_quiz.html'
  - Most Templates are short with basic HTML, however there are a few that include JavaScript.  These are 'create_quiz.html' and 'edit_quiz.html'
  	- Editing the functionality of these two pages must be done in JS.
+++++++++++++++++++++++++++++++++++++++++++++++++
Forms
  - Forms Allow user interaction in specific pages
  - within forms, you will find the logic for password resets, login, manual add question, and sign-ups
+++++++++++++++++++++++++++++++++++++++++++++++++
urls
  - The urls.py file contains the url mapping for each page
+++++++++++++++++++++++++++++++++++++++++++++++++
tests
  - tests.py is where you will find all available tests for each working part in the program
	- to run tests, run [python varient] manage.py test
