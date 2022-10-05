from flask import request, render_template, redirect, url_for, session, flash
import csv
import pandas as pd
from random import randint
from testing_app import app, db, client
from testing_app.models import CFV
from pymongo.errors import ConnectionFailure

@app.route("/", methods=["GET"])
def index():
    try: 
        client.my_db.command('ping')
        
    except ConnectionFailure:
        return render_template("index.html", msg="The service could not connect to the db")
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        format = CFV.valid_creds(email, username, password)
        if format == "Success":
            generate_new = 6
            collection = db["Creds"]
            results = collection.find({"username": str(username), "email": str(email)})
            validity = []
            for result in results:
                validity.append(result)
            credentials = {
                "_id": generate_new,
                "username": username,
                "password": password,
                "email": email,
                "role": role
            }                      
            if len(validity) != 0:
                collection.insert_one(credentials)
                return redirect(url_for('login'))
            else:
                flash("That email/user is already in use!")
        else:
            for message in format:
                if message != "Success":
                    flash(message)
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        collection = db["Creds"]
        results = collection.find({"username": username, "password": password})
        validity = []
        for result in results:
            validity.append(result)
        if len(validity) > 0:
            session["user"] = username
            session["role"] = validity[0]["role"]
            role = session["role"]
            if role == "student":
                return redirect(url_for("student"))
            if role == "teacher":
                return redirect(url_for("teacher"))
            if role == "admin":
                return redirect(url_for("admin"))
        else:
            flash("Incorrect username/password. Try again!")
            return render_template("login.html")
    else:
        return render_template("login.html")


@app.route("/teacher", methods=['GET','POST'])
def teacher():
    if request.method == "POST":
        uploaded_data = request.files['questions']
        df = pd.read_csv(uploaded_data)
        df["user_id"] = session["user"]
        test_id = str(randint(100000,999999))
        df["test_id"] = test_id
        df.to_csv("questions.csv", index=False)
        header = ["question", "answer", "option1", "option2", "option3", "user_id", "test_id"]
        csvfile = open("questions.csv", 'r')
        reader = csv.DictReader(csvfile)
        collection = db["QuestionBank"]
        for each in reader:
            row = {}
            for field in header:
                row[field]=each[field]
            collection.insert_one(row)
        return render_template("base_landing.html", msg=f"Your test ID is {test_id}")    
    else:
        if session["role"] == "teacher":
            return render_template("teacher_landing.html")
        elif session["role"] == None:
            return redirect(url_for("login"))
        else:
            return redirect(url_for(f"{session['role']}"))


@app.route("/student", methods=['GET','POST'])
def student():
    if request.method == "POST":
        test = request.form["test_id"]
        session["test_id"] = test
        return redirect(url_for("quiz", test_id=test))
    else:
        if session["role"] == "student":
            return render_template("student_landing.html")
        elif session["role"] == None:
            return redirect(url_for("login"))
        else:
            return redirect(url_for(f"{session['role']}"))


@app.route("/logout")
def logout():
    if "user" in session:
        flash("You have been logged out successfully", "info")
    session.pop("user", None)
    session.pop("role", None)
    return redirect(url_for("login"))


@app.route("/landing")
def landing():
    return render_template("base_landing.html")


@app.route("/quiz/<test_id>")
def quiz(test_id):
    if session["test_id"] == test_id:
        collection = db["QuestionBank"]
        cursor = collection.find({"test_id": test_id})
        questions = []
        count = 1
        for question in cursor:
            question["qnum"] = count
            count += 1
            questions.append(question)        
        return render_template("quiz.html", array=questions, max_list=count-1)
    else:
        return render_template("index.html", msg = "The quiz has timed out")


@app.route("/submit", methods=["GET","POST"])
def submit():
    if request.method == "POST":
        no_answers = request.form["max_list"]
        score = 0
        for i in range(1, int(no_answers) + 1):
            if request.form[f"mcq{i}"] == request.form[f"crct{i}"]:
                score += 1
        result = f"{100* int(score)/int(request.form['max_list'])}%"
    session.pop("test_id", None)
    return render_template("summary.html", answer_one=result)