from flask import Flask, redirect, render_template, request, session, escape
from functools import wraps
from helpers import apology, login_required, matching_algorithm
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3 
import os
import time
import jinja2

#Configure application 
app = Flask(__name__)

##Configure Session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



data = sqlite3.connect('qbspark.db', check_same_thread=False)
db = data.cursor()

#Create users table to keep track of all mentors and mentees
#Will be used to validate login attempts 
#Create 

# List of QB schools b/c listing them in survey would be too long and also QB schools have big potential to change
schools = ["Amherst College", "Barnard College", "Boston College", "Boston University", "Bowdoin College","Brown University",
"California Institute of Technology","Carleton College","Claremont McKenna College","Colby College","Colgate University",
"Colorado College","Columbia University","Dartmouth College","Davidson College","Denison University","Duke University","Emory University",
"Grinnell College","Hamilton College","Haverford College","Macalester College","Massachusetts Institute of Technology","Northwestern University",
"Oberlin College","Pomona College","Princeton University","Rice University","Scripps College","Stanford University","Swarthmore College",
"Tufts University","University of Chicago","University of Notre Dame","University of Pennsylvania","University of Southern California",
"University of Virginia","Vanderbilt University","Vassar College","Washington and Lee University","Washington University in St. Louis",
"Wellesley College","Wesleyan University","Williams College","Yale University"]

app.config["TEMPLATES_AUTO_RELOAD"] = True


#Routes
@app.route('/')
def hello():
    return render_template("home1.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    """log in the user"""
    ##If the method is post, then go to the dashboard of mentor or mentee
    if request.method == "GET":
        return render_template("login.html")
    else: 
        username = request.form.get("username")
        role = request.form.get("role")
        rows = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()
        check = db.execute("SELECT COUNT(username) FROM users WHERE username = ?", (username,)).fetchall()
        data.commit()

        if check[0][0] == 0:
            return apology("incorrect username. username does not exist.")
        #Assign the session user id
        session["user_id"] = rows[0][0]
        if role == "mentor":
            session["role"] = "mentor"
            return redirect("/mentorDashboard")
        else: 
            session["role"] = "mentee"
            return redirect("/menteeDashboard")

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

@app.route('/register', methods=["GET", "POST"])
def register():
    """Register users"""
    session.clear()
    if request.method == "GET":
        return render_template("register.html")
    else:
        role = request.form.get("role")
        username = request.form.get("username")
        confirmation = request.form.get("confirmation")
        password = request.form.get("password")
        email = request.form.get("email")
        discord = request.form.get("discord")

        if password != confirmation:
            return apology("Your password confirmation does not match your password. Try again.")
        
        #Check registration information then send to respective surveys 
        if role == "Mentor":
            rows = db.execute("SELECT * FROM users WHERE username = ?", (username,))
            # check_registration(rows, username, password, confirmation)
            db.execute("INSERT INTO users (username, password, email, discord, role) VALUES (?,?,?,?,?)", (username, generate_password_hash(password), email, discord, 1))
            new = db.execute("SELECT * FROM users WHERE username = ?", (username,))
            session["user_id"] = new.fetchall()[0][0]
            session["role"] = "mentor"
            data.commit()
            return redirect("/mentorSurvey")
        else:
            rows = db.execute("SELECT * FROM users WHERE username = ?", (username,))
            # check_registration(rows, username, password, confirmation)
            db.execute("INSERT INTO users (username, password, email, discord, role) VALUES (?,?,?,?,?)", (username, generate_password_hash(password), email, discord, 0))
            new = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()[0][0]
            session["user_id"] = new
            session["role"] = "mentee"
            data.commit()
            return redirect("/menteeSurvey")

#making sure to pass on the list of schools to the html for the mentees and mentors surveys
@app.route('/menteeSurvey', methods=["GET", "POST"])
def surveyMentee():
    if request.method == "GET":
        return render_template("menteeSurvey.html", schools=schools)
    else:
        user_id = session["user_id"]
        #Store terms and conditions data 
        term_one = request.form.get("term_one")
        term_two = request.form.get("term_two")
        term_three = request.form.get("term_three")
        term_four = request.form.get("term_four")
        # db.execute("INSERT INTO users (term_one, term_two, term_three, term_four) VALUES (?,?,?,?) WHERE id = ?", (term_one, term_two, term_three, term_four, user_id))
        ##TODO Check that the terms and conditions are all agree statements. 

        #Store survey data about ethnic background
        ethnicity = request.form.get("ethnicity")
        db.execute("INSERT INTO ethnicity (person_id, ethnicity) VALUES (?,?)", (user_id, ethnicity))

        #Store survey data about religious background
        religion = request.form.get("religion")
        db.execute("INSERT INTO religion (person_id, religion) VALUES (?,?)", (user_id, religion))

        #Store survey data about gender identity
        gender = request.form.get("gender")
        db.execute("INSERT INTO gender (person_id, gender) VALUES (?,?)", (user_id, gender))
        
        #Store survey data about citzenship status
        citizenship = request.form.get("citizenship")
        db.execute("INSERT INTO citizenship (person_id, citizenship) VALUES (?,?)", (user_id, citizenship))

        #Store survey data about academic pathway
        academic_pathway = request.form.get("academics")
        db.execute("INSERT INTO academics (person_id, academic_pathway) VALUES (?,?)", (user_id, academic_pathway))

        #Store rankings 
        academic_rank = request.form.get("academicrank")
        gender_rank = request.form.get("genderrank")
        religion_rank = request.form.get("religionrank")
        ethnicity_rank = request.form.get("racerank")
        citizenship_rank = request.form.get("citizenshiprank")
        db.execute("INSERT INTO rankings (person_id, academics, gender, religion, ethnicity, citzenship) VALUES (?,?,?,?,?,?)", (user_id, academic_rank, gender_rank, religion_rank, ethnicity_rank, citizenship_rank))
        # Store bio information
        bio = request.form.get("bio")
        school1 = request.form.get("school1")
        school2 = request.form.get("school2")
        school3 = request.form.get("school3")
        db.execute("UPDATE users SET bio = (?), school1 = ?, school2 = ?, school3 = ? WHERE id = ?", (bio, school1, school2, school3, user_id))

        data.commit()

        #Run the matching algorithm so that mentee gets a mentor
        matching_algorithm(user_id)
        return redirect("/menteeDashboard")

@app.route('/mentorSurvey', methods=["GET", "POST"])
def surveyMentor():
    if request.method == "GET":
        return render_template("mentorSurvey.html")
    else:
        user_id = session["user_id"]

        #Store terms and conditions data 
        term_one = request.form.get("term_one")
        term_two = request.form.get("term_two")
        term_three = request.form.get("term_three")
        term_four = request.form.get("term_four")
        term_five = request.form.get("term_five")
        # db.execute("INSERT INTO users (term_one, term_two, term_three, term_four, term_five) VALUES (?,?,?,?,?) WHERE id = ?", (term_one, term_two, term_three, term_four, term_five, user_id))
        ##TODO Check that the terms and conditions are all agree statements. 

        #Store survey data about ethnic background
        ethnicity = request.form.get("ethnicity")
        db.execute("INSERT INTO ethnicity (person_id, ethnicity) VALUES (?,?)", (user_id, ethnicity))

        #Store survey data about religious background
        religion = request.form.get("religion")
        db.execute("INSERT INTO religion (person_id, religion) VALUES (?,?)", (user_id, religion))

        #Store survey data about gender identity
        gender = request.form.get("gender")
        db.execute("INSERT INTO gender (person_id, gender) VALUES (?,?)", (user_id, gender))
        
        #Store survey data about citzenship status
        citizenship = request.form.get("citizenship")
        db.execute("INSERT INTO citizenship (person_id, citizenship) VALUES (?,?)", (user_id, citizenship))

        #Store survey data about academic pathway
        academic_pathway = request.form.get("academics")
        db.execute("INSERT INTO academics (person_id, academic_pathway) VALUES (?,?)", (user_id, academic_pathway))

        #Store mentee_count
        mentee_count = request.form.get("menteecount")
        db.execute("INSERT INTO mentee_count (person_id, mentee_count, mentees_left) VALUES (?,?,?)", (user_id, mentee_count, mentee_count))
        data.commit()

        #Store bio information
        current = request.form.get("current")
        bio = request.form.get("bio")
        db.execute("INSERT INTO users (bio, school1, school2, school3) VALUES (?,?,?,?) WHERE id = ?", (bio, current, "N/A", "N/A", user_id))

        
        return redirect("/mentorDashboard")
        # return render_template("mentorDashboard.html")

@login_required
@app.route('/mentorDashboard', methods=["GET", "POST"])
def mentorDashboard():
    if request.method == "GET":
        # Information for the meetings table
        # mentee_id = db.execute("SELECT mentee_id FROM matches WHERE mentor_id = ? ", (session["user_id"], )).fetchall()[0][0]
        
        meets = db.execute("SELECT * FROM meets WHERE sender = (SELECT username FROM users WHERE id = ?) OR receiver = (SELECT username FROM users WHERE id = ?)", (session["user_id"], session["user_id"], ) ). fetchall()
        mymentees = db.execute("SELECT username, bio, school1, school2, school3, email  FROM users WHERE id IN (SELECT mentee_id FROM matches WHERE mentor_id = ?)", (session["user_id"], )).fetchall()
        email = db.execute("SELECT email FROM users WHERE id IN (SELECT mentee_id FROM matches WHERE mentor_id = ?)", (session["user_id"], )).fetchall()
        bios = db.execute("SELECT school1 FROM users WHERE id IN (SELECT mentee_id FROM matches WHERE mentor_id = ?)", (session["user_id"], )).fetchall()
        # Todo: add the bio! 

        data.commit()
        # print("meets", meets)
        # print("email", email)
        print("bios,", mymentees)

        return render_template("mentorDashboard.html", email = email, mymentees=mymentees, meets=meets, bios=bios)

@login_required
@app.route('/mentorProfile', methods=["GET", "POST"])
def mentorProfile():
    if request.method == "GET":
        return render_template("mentorProfile.html")

@login_required
@app.route('/menteeDashboard', methods=["GET", "POST"])
def menteeDashboard():
    if request.method == "GET":
        id = session["user_id"]
        print("session role", session["role"])
        mentor_id = db.execute("SELECT mentor_id FROM matches WHERE mentee_id = ? ", (id,)).fetchall()
        mentor_name = db.execute("SELECT username FROM users WHERE id = ?", mentor_id[0]).fetchall()[0][0]
        mentor_email = db.execute("SELECT email FROM users WHERE id = ?", mentor_id[0]).fetchall()[0][0]
        mentor_bio = db.execute("SELECT bio FROM users WHERE id = ?", mentor_id[0]).fetchall()[0][0]
        mentor_school = db.execute("SELECT school1 FROM users WHERE id = ?", mentor_id[0]).fetchall()[0][0]
        # Information for the meetings table
        meets = db.execute("SELECT * FROM meets WHERE sender = (SELECT username FROM users WHERE id = ?) OR receiver = (SELECT username FROM users WHERE id = ?)", (session["user_id"], session["user_id"], ) ). fetchall()
        return render_template("menteeDashboard.html", meets=meets, mentor_name = mentor_name, mentor_email = mentor_email, mentor_bio=mentor_bio, mentor_school=mentor_school)

@login_required
@app.route('/menteeProfile', methods=["GET", "POST"])
def menteeProfile():
    if request.method == "GET":
        return render_template("menteeProfile.html")

@login_required
@app.route('/schedulerMentor', methods=["GET", "POST"])
def schedulerMentor():
    if request.method == "GET":
        # Making sure to have a list of corresponding mentees to schedule with
        mymentees = db.execute("SELECT username FROM users WHERE id IN (SELECT mentee_id FROM matches WHERE mentor_id = ?)", (session["user_id"], ))
        return render_template("schedulerMentor.html", mymentees = mymentees)
    else:
        # Transfering data into table for meeting times
        link = request.form.get("link")
        # print("linkkkk,", link)
        date = request.form.get("date")
        # print("linkkkk,", date)
        time = request.form.get("time")
        # print("linkkkk,", time)
        receiver = request.form.get("who")
        sender = db.execute("SELECT username FROM users WHERE id = ?", (session["user_id"], )).fetchall()

        db.execute("INSERT INTO meets (sender, receiver, date, time, link) VALUES (?,?,?,?,?)", (sender[0][0], receiver, date, time, link))
        data.commit()
        return redirect("/mentorDashboard")


@login_required
@app.route('/schedulerMentee', methods=["GET", "POST"])
def schedulerMentee():
    if request.method == "GET":
        return render_template("schedulerMentee.html")
    else:
        link = request.form.get("link")
        date = request.form.get("date")
        time= request.form.get("time")
        receiver = db.execute("SELECT username FROM users WHERE id = (SELECT mentor_id FROM matches WHERE mentee_id = ?)", (session["user_id"], )).fetchall()
        sender = db.execute("SELECT username FROM users WHERE id = ?", (session["user_id"], )).fetchall()
        db.execute("INSERT INTO meets (sender, receiver, date, time, link) VALUES (?,?,?,?,?)", (sender[0][0], receiver[0][0], date, time, link))
        data.commit()
        return redirect("/menteeDashboard")

@login_required
@app.route('/notes', methods=["GET", "POST"])
def notesMentor():
    if request.method == "GET":
        return render_template("notes.html")

@login_required
@app.route('/resourcesMentor', methods=["GET", "POST"])
def resourcesMentor():
    if request.method == "GET":
        return render_template("resourcesMentor.html")

@login_required
@app.route('/resourcesMentee', methods=["GET", "POST"])
def resourcesMentee():
    if request.method == "GET":
        return render_template("resourcesMentee.html")