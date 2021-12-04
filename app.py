from flask import Flask, redirect, render_template, request, session
# from helpers import matching_algorithm
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3 
import os

app = Flask(__name__)
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

@app.route('/')
def hello():
    return render_template("home.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    """log in the user"""
    ##If the method is post, then go to the dashboard of mentor or mentee
    if request.method == "GET":
        return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def registerMentee():
    """Register users"""
    ##Must also check that a user is not signing up twice. 
    if request.method == "GET":
        return render_template("register.html")
    else:
        role = request.form.get("role")
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        discord = request.form.get("discord")

        if role == "Mentor":
            db.execute("INSERT INTO mentors (username, password, email, discord) VALUES (?,?,?,?)", (username, password, email, discord))
            data.commit()
            return render_template("mentorSurvey.html")
        else:
            db.execute("INSERT INTO mentees (username, password, email, discord) VALUES (?,?,?,?)", (username, password, email, discord))
            data.commit()
            return render_template("menteeSurvey.html")


#making sure to pass on the list of schools to the html for the mentees and mentors surveys
@app.route('/menteeSurvey', methods=["GET", "POST"])
def surveyMentee():
    """Register a Mentor"""
    if request.method == "GET":
        return render_template("menteeSurvey.html", schools=schools)
    #if the next button is clicked + the role selected is mentee

@app.route('/mentorSurvey', methods=["GET", "POST"])
def surveyMentor():
    if request.method == "GET":
        return render_template("mentorSurvey.html")
    ##if next button is clicked + the role selected is mentor

# @login_required
@app.route('/mentorDashboard', methods=["GET", "POST"])
def mentorDashboard():
    if request.method == "GET":
        return render_template("mentorDashboard.html")

# @login_required
@app.route('/mentorProfile', methods=["GET", "POST"])
def mentorProfile():
    if request.method == "GET":
        return render_template("mentorProfile.html")

# @login_required
@app.route('/menteeDashboard', methods=["GET", "POST"])
def menteeDashboard():
    if request.method == "GET":
        return render_template("menteeDashboard.html")

# @login_required
@app.route('/menteeProfile', methods=["GET", "POST"])
def menteeProfile():
    if request.method == "GET":
        return render_template("menteeProfile.html")

