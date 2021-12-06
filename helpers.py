import os 
from functools import wraps
from flask import render_template, escape, session, redirect
import urllib.parse
import sqlite3

data = sqlite3.connect('qbspark.db', check_same_thread=False)
db = data.cursor()

def apology(message):
    return render_template("apology.html", bottom=escape(message))

def login_required(f):
    """
    Check to see if a user is logged in or not.
    Will redirect user to login page if they are not a user 
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def check_registration(rows, username, password, confirmation):
    if username == "" or password == "" or confirmation == "":
        return apology("Must input username, password, and confirmation")
    elif password != confirmation:
        return apology("Password and confirmation do not match")
    elif rows.rowcount() != 0: 
        return apology("Username already taken.")


def matching_algorithm():
# Create a list of mentees to go through, using only user id
    mentees = []
    mentees = db.execute("SELECT id FROM users WHERE role = ?", (0))
# Create a list of mentors to go through, using only user id
    mentors = []
    mentors = db.execute("SELECT id FROM mentors")
    for mentee in mentees:
        # Compatibitility trackers that store compatibility scores and the id of the mentor for that score
        oldcompatibility = []
        newcompatibility = []
        oldcompatibility [0] = 0
        newcompatibility [0] = 0
        # Select the current mentee's category ranking (which is stored as a weight)
        academics = db.execute("SELECT academics FROM rankings WHERE person_id = ?", (mentee))
        gender = db.execute("SELECT gender FROM rankings WHERE person_id = ?", (mentee))
        religion = db.execute("SELECT religion FROM rankings WHERE person_id = ?", (mentee))
        ethnicity = db.execute("SELECT ethnicity FROM rankings WHERE person_id = ?", (mentee))
        citizenship = db.execute("SELECT citizenship FROM rankings WHERE person_id = ?", (mentee))
        # This is where the algorithm will check if a mentor has spots available
        for mentor in mentors:
            if db.execute("SELECT mentees_left  FROM mentee_count WHERE person_id = ?", (mentor)) == 0:
                break
            else:
                # This is where we will start the comparisons, comparing the answers between each mentee with each mentor for each ranked category
                for mentor in mentors:
                    academicsmatch = db.execute("SELECT academic_pathway FROM academics WHERE person_id = ? EXISTS (SELECT academic_pathway FROM academics WHERE person_id = ?)", (mentee, mentor))
                    if academicsmatch == True:
                        academicsmatch = 1
                    else:
                        academicsmatch = 0
                    gendermatch = db.execute("SELECT gender FROM gender WHERE person_id = ? EXISTS (SELECT gender FROM gender WHERE person_id = ?)", (mentee, mentor))
                    if gendermatch == True:
                        gendermatch = 1
                    else:
                        gendermatch = 0
                    religionmatch = db.execute("SELECT religion FROM religion WHERE person_id = ? EXISTS (SELECT religion FROM religion WHERE person_id = ?)", (mentee, mentor))
                    if religionmatch == True:
                        religionmatch = 1
                    else:
                        religionmatch = 0
                    citizenshipmatch = db.execute("SELECT citizenship FROM citizenship WHERE person_id = ? EXISTS (SELECT citizenship FROM citizenship WHERE person_id = ?)", (mentee, mentor))
                    if citizenshipmatch == True:
                        citizenshipmatch = 1
                    else:
                        citizenshipmatch = 0
                    # Ethnicity is multiple select, so the process is a bit different
                    # We will see if each option is checked or not in mentee and mentor side, then compute a correctness fraction
                    # The correctness fraction (called "ethnicitymatch") should be sum of all matched selection status of option/ total options
                    ethnicitymatch1 = db.execute("SELECT COUNT(black) FROM ethnicity WHERE person_id = ? OR person_id = ?", (mentee, mentor)) + 1
                    ethnicitymatch2 = db.execute("SELECT COUNT(asian) FROM ethnicity WHERE person_id = ?) = (SELECT asian FROM ethnicity WHERE person_id = ?))", (mentee, mentor)) + 1
                    ethnicitymatch3 = db.execute("SELECT COUNT(american_india) FROM ethnicity WHERE person_id = ? OR person_id = ?", (mentee, mentor)) + 1
                    ethnicitymatch4 = db.execute("SELECT COUNT(pacific_islander) FROM ethnicity WHERE person_id = ? OR person_id = ?", (mentee, mentor)) + 1
                    ethnicitymatch5 = db.execute("SELECT COUNT(white) FROM ethnicity WHERE person_id = ? OR person_id = ?", (mentee, mentor)) + 1
                    ethnicitymatch6 = db.execute("SELECT COUNT(latinx) FROM ethnicity WHERE person_id = ? OR person_id = ?", (mentee, mentor)) + 1
                    ethnicitymatch7 = db.execute("SELECT COUNT(none) FROM ethnicity WHERE person_id = ? OR person_id = ?", (mentee, mentor)) + 1
                    ethnicitymatch = (ethnicitymatch1%2 + ethnicitymatch2%2 + ethnicitymatch3%2 + ethnicitymatch4%2 + ethnicitymatch5%2 + ethnicitymatch6%2 + ethnicitymatch7%2)/7

                    # Compute a new compatibility score to store the current calculation
                    newcompatibility = (academics * academicsmatch) + (religion * religionmatch) + (citizenship * citizenshipmatch) + (gender * gendermatch) + (ethnicity * ethnicitymatch)
                    # If this new compatibility score is higher than that of the mentee's and the previous mentor, exchange the old compatibility with the new
                    # This way we ensure that at the end, the old compatibility is the highest found score combination for mentee and mentor pair
                    if newcompatibility[0] > oldcompatibility[0] or newcompatibility[0] == oldcompatibility[0] : 
                        oldcompatibility[0] = newcompatibility[0]
                        oldcompatibility[1] = mentee
                        oldcompatibility[2] = mentor
                # Insert highest score and match information into database
                db.execute("INSERT INTO matches (score, mentee_id, mentor_id) VALUES (?,?,?)", (oldcompatibility[0], oldcompatibility[1], oldcompatibility[2]))
                # Update the mentee count
                beforecount = db.execute("SELECT mentees_left FROM mentee_count WHERE person_id = ?", (oldcompatibility[2]))
                db.execute("UPDATE mentee_count SET mentees_left = ? WHERE person_id = ?", ((beforecount-1), oldcompatibility[2]))
                

#     #If there are no mentors, put mentee on waiting list table. 
    
