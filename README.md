# Testing Platform Project

## How to run the app

1. Install the repository
2. Run `pip install .`
3. Follow mongo-setup.md
4. Set the environment variable `export DB_HOST=db_ip_address` the db ip address is the ip address of the server where the DB is running
5. `python app.py` runs the app.

## Description

>A testing platform which will be used to test students on their knowledge of varied subject areas. The administrator controls the test questions, the program should find the solution to the question and match that against the students answers when they come to answer the test.
>
>The application should be a pop-out interactive screen and should take a login. The application should then review a database of login credentials which will inform if the user is an administrator or a student and hence redirect them accordingly.
>
>If the administrator creates a new test then an 8-digit randomised test code should be created which can be shared with the students.
>
>Students who log in should be greeted with a box to enter their test code where they will be redirected to their test


![user_diagram](https://user-images.githubusercontent.com/110126036/193938347-af52c5aa-3641-4b00-b68b-265b0a304698.PNG)


## User Stories

Provides general guidance on what the different users are supposed to do using the application.

### Administrator

The administrator needs to:

- Access administrator privileges (using a login)
- Upload questions to be tested 
- Remove questions to be tested
- Share the test code

### Teacher

The teacher needs to:

- Access teacher privileges (using a login)
- Access student screen
- Upload questions to be tested 
- Remove questions from their own tests (that they created)
- Share the test code


### Student

The user must be able to:

- Access the test (using a login)
- Answer the test (using a test-code)
- Answers must be abstracted from them
- Receive a score on the outcome of the test
- See which questions were answered incorrectly / correctly
- Receive brief explanation on the solution (to relay to the student)
- Share the score with the admin automatically.

#
# Specific Features

What are the features of the app? We can then split the different sections for a microservice architecture. The tools to implement the solution used can be changed at a later date.

![architecture](https://user-images.githubusercontent.com/110126036/193938296-977871fd-d2b1-489f-861a-59bb52b3d6e2.png)

NOTE: Each box should be contained within its own container, with the exception of the frontend and backend website which both share a container.

#
## Login Page - Frontend/Backend Website
### Description

Allows the user to access the appropriate page and permissions relative to their role. Backend written in Flask. Front end written in HTML and CSS.

### Features
1. User should be given two boxes login / password 
2. Access the credentials database after user presses login button
3. Receives validation of credentials from credentials database
   1. Receives data on if user is admin / student
   2. Sends to admin / student screens 
4. If validation is incorrect refresh the login page (to refresh the entered fields)
5. Provides a sign up button which redirects to the sign up page
6. Should create a session for the user so they can use the site freely

#
## Sign-up page - Frontend/Backend website
### Description

Gives the user the ability to create an account (so they are able to access appropriate access rights). The ability of teacher is granted in this page because the teacher has the ability to delete only their work. Users can apply for an admin account (teachers who sign up cannot damage the website). Front-end in HTML and CSS. Backend in Flask.

### Features
1. Asks for username
2. Asks for email
3. Asks for password and repeated password
4. Asks if student / teacher
5. Adds data to credentials database (if username is not pre-existing)
6. Redirects back to login page once signed up
7. Provides option to return to sign in page

#### NOTE MFA option can be added to this at a later date along with email verification

#
## Credentials database - Credentials MS SQLServer
### Description

Stores the user's data who have created an account. Used to validate/invalidate sign in attempts. Written in SQL language because the data is heavily structured and to ensure data validity.

Contains fields for the following:
- user_id
- user_name
- email
- password
- role

REST API to sit in front of database to handle requests.

#### MFA Boolean value can be added at a later date (along with email verified)

#
## Student screen 
### Description

Condition: IFF logged in & role = student. Students should be able to take tests set by teachers/admins.

### Features
- Student can enter an 8-digit code
- If the code matches the test code in the test bank then redirect to the test page

## Teacher screen 
### Description 

Condition: IFF logged in & role = teacher. Should be able to create the tests for students to use, also be able to delete their own tests. They should also be able to sit tests.

### Features:
- Inherits the student functionality
- Allows for the creation of tests
- Once a test is created it is run and the results are stored in the test bank (this is so that the test only has to be ran once rather than on everytime a student wants to complete a test)
- Teachers can view the tests they created and delete/edit accordingly


## Admin screen
### Description

Condition IFF logged in & role = admin. Allows the admin to delete any tests from the test bank. Also are able to sit any tests/ create tests.

### Features
- Inherits teacher functionality except can view all tests and delete/edit accordingly

#
## Test bank (MongoDB)

Stores unstructured data in the form of tests. Holds the creators user_id and takes a random test ID which can be used by students to access the test. The questions and answers are also included.

Example structure for question bank:

{
   "owner_id": 231,
   "test_id": 2313121,
   "questions": {
      "what is 2*4": 8,
      "Who wrote Hamilton": "Shakespeare", 
      "what is 6*8": [48,32,12,23]
   }
}

Extra table included for results

Example structure:

{
   "owner_id": 231,
   "test_id": 2313121,
   "results": {
      "student1_id": 80
      "student2_id": 54
   }
}

REST API to sit in front of the database to handle requests.

#
## Testing Screen
### Description

Should upload the questions from the database, based on the user's input. Randomising the order of the questions in which they appear and also displaying a box where they can enter their results.

If the question has a key-value pair of a list then a radio button should be used to select the correct answer.

### Features
- Retrieves relevant questions
- Randomises the order
- Displays question
- Displays answer box
- Displays next button or previous button to go to the next question
- Displays finish test button on the last page
- Directs to summary page

#
## Test Creating Screen
### Description

Gives teachers the choice to either upload a CSV or use an interactive mode (which would append questions to a csv in the backend).

If giving the student a multiple choice question then the correct answer should be stored in the first index(so it can be matched against the students answer).

### Features
- Allows for the upload of a CSV
- Allows the user to append questions to a html form
- Configure appended questions to a csv (from the form)
- Post the csv to mongodb

#
## Summary page
Displays when the student completes a test. Shows the student their score. Should also store the result in mongodb which can then be retrieved by the test creator and themselves at a later date.

###
- Displays score
- Stores their result in mongodb (to be reviewed by teacher or by themselves at a later date)

#
## Results Page
### Description

Shows the user all of the previous tests that they have taken and their respective score next to it. For teachers/admins should should show all of the tests that they have access to (for admin should be all tests) and within this they can see the results and associated usernames.

### Features

- Directory system for admin/teachers
- Displays results of users(from mongodb)


