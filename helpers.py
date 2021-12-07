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


def matching_algorithm(mentee_id):
    mentees = db.execute("SELECT id FROM users WHERE role = ?", (0, ))
<<<<<<< HEAD
=======
    mentors = db.execute("SELECT id FROM users WHERE role = ?", (1, ))
    
    # Count the number of mentors in the database
>>>>>>> b78d7f16b33c299ac5e85e7318118183ff0665e8
    mentors = db.execute("SELECT id FROM users WHERE role = ?", (1, ))
    print(len(mentors.fetchall()))
    print("TEST")

    #Count the number of mentors in the database
<<<<<<< HEAD
=======
    cmentors = db.execute("SELECT * FROM users WHERE role = ?", (1, )).fetchall()
    print("TEST BEFORE", cmentors)
    mentor_count = int(len(cmentors))
    # print("mentor_count start", mentor_count)
>>>>>>> b78d7f16b33c299ac5e85e7318118183ff0665e8
    cmentors = db.execute("SELECT * FROM users WHERE role = ?", (1, ))
    mentor_count = cmentors.rowcount
    status = 1

    # Compatibitility trackers store match score, mentee_id, and mentor_id
    oldcompatibility = [0,0,0]
    newcompatibility = [0,0,0]
    mentee_id = str(mentee_id)
    print("start", oldcompatibility[0], oldcompatibility[1], oldcompatibility[2])

    # Store mentee's category weights 
    academics = db.execute("SELECT academics FROM rankings WHERE person_id = ?", (mentee_id, ))
    gender = db.execute("SELECT gender FROM rankings WHERE person_id = ?", (mentee_id, ))
    religion = db.execute("SELECT religion FROM rankings WHERE person_id = ?", (mentee_id, ))
    ethnicity = db.execute("SELECT ethnicity FROM rankings WHERE person_id = ?", (mentee_id, ))
    citizenship = db.execute("SELECT citzenship FROM rankings WHERE person_id = ?", (mentee_id, ))
    
    print("TEST AFTER", cmentors)
    for mentor in cmentors:
        print("INSIDE")
        mentor = str(mentor)
        #If there are mentors left, calculate scores 
        if mentor_count > 0: 
            #If mentor has mentee spots left, calculate match scores. 
            if db.execute("SELECT mentees_left FROM mentee_count WHERE person_id = ?", (mentor, )) == 0:
                mentor_count = mentor_count - 1
            else:
                #Set category match score to 1 if there is match and 0 if not 
                academicsmatch1 = db.execute("SELECT academic_pathway FROM academics WHERE person_id = ?", (mentee_id,)).fetchall()
                academicsmatch2 = db.execute("SELECT academic_pathway FROM academics WHERE person_id = ?", (mentor, )).fetchall()
                
                if academicsmatch1[0][1] == academicsmatch2[0][1]:
                    academicsmatch = 1
                else:
                    academicsmatch = 0

                gendermatch = db.execute("SELECT gender FROM gender WHERE person_id = ? EXISTS (SELECT gender FROM gender WHERE person_id = ?)", (mentee_id, mentor, ))
                if gendermatch == True:
                    gendermatch = 1
                else:
                    gendermatch = 0

                religionmatch = db.execute("SELECT religion FROM religion WHERE person_id = ? EXISTS (SELECT religion FROM religion WHERE person_id = ?)", (mentee_id, mentor, ))
                if religionmatch == True:
                    religionmatch = 1
                else:
                    religionmatch = 0

                citizenshipmatch = db.execute("SELECT citizenship FROM citizenship WHERE person_id = ? EXISTS (SELECT citizenship FROM citizenship WHERE person_id = ?)", (mentee_id, mentor, ))
                if citizenshipmatch == True:
                    citizenshipmatch = 1
                else:
                    citizenshipmatch = 0

                # Ethnicity has a different process because of multi-select
                # We will see if each option is checked or not in mentee and mentor side, then compute a correctness fraction
                # The correctness fraction (called "ethnicitymatch") should be sum of all matched selection status of option/ total options
                ethnicitymatch1 = db.execute("SELECT COUNT(black) FROM ethnicity WHERE person_id = ? OR person_id = ?", (mentee_id, mentor, )) + 1
                ethnicitymatch2 = db.execute("SELECT COUNT(asian) FROM ethnicity WHERE person_id = ?) = (SELECT asian FROM ethnicity WHERE person_id = ?))", (mentee_id, mentor, )) + 1
                ethnicitymatch3 = db.execute("SELECT COUNT(american_india) FROM ethnicity WHERE person_id = ? OR person_id = ?", (mentee_id, mentor, )) + 1
                ethnicitymatch4 = db.execute("SELECT COUNT(pacific_islander) FROM ethnicity WHERE person_id = ? OR person_id = ?", (mentee_id, mentor, )) + 1
                ethnicitymatch5 = db.execute("SELECT COUNT(white) FROM ethnicity WHERE person_id = ? OR person_id = ?", (mentee_id, mentor, )) + 1
                ethnicitymatch6 = db.execute("SELECT COUNT(latinx) FROM ethnicity WHERE person_id = ? OR person_id = ?", (mentee_id, mentor, )) + 1
                ethnicitymatch7 = db.execute("SELECT COUNT(none) FROM ethnicity WHERE person_id = ? OR person_id = ?", (mentee_id, mentor, )) + 1
                ethnicitymatch = (ethnicitymatch1%2 + ethnicitymatch2%2 + ethnicitymatch3%2 + ethnicitymatch4%2 + ethnicitymatch5%2 + ethnicitymatch6%2 + ethnicitymatch7%2)/7

                # Compute a new compatibility score to store the current calculation
                newcompatibility[0] = (academics * academicsmatch) + (religion * religionmatch) + (citizenship * citizenshipmatch) + (gender * gendermatch) + (ethnicity * ethnicitymatch)
                
                # If this new compatibility score is higher than that of the mentee's and the previous mentor, exchange the old compatibility with the new
                # This way we ensure that at the end, the old compatibility is the highest found score combination for mentee and mentor pair
                if newcompatibility[0] > oldcompatibility[0] or newcompatibility[0] == oldcompatibility[0]: 
                    oldcompatibility[0] = newcompatibility[0]
                    oldcompatibility[1] = mentee_id
                    oldcompatibility[2] = mentor
        else:
            #otherwise, put mentees onto a waitlist
            db.execute("INSERT INTO matches (score, mentee_id, mentor_id) VALUES (?,?,?)", (0, mentee_id, 0))
            status = 0    
       
        # Insert highest score and match information into database
        print("final thing to push to matches", oldcompatibility[0], oldcompatibility[1], oldcompatibility[2])
        db.execute("INSERT INTO matches (score, mentee_id, mentor_id) VALUES (?,?,?)", (oldcompatibility[0], oldcompatibility[1], oldcompatibility[2], ))
        # Update the mentee count
        # current_count = db.execute("SELECT mentees_left FROM mentee_count WHERE person_id = ?", (oldcompatibility[2], ))
        # current_count = current_count.fetchall()[0] - 1
        db.execute("UPDATE mentee_count SET mentees_left = mentees_left - 1 WHERE person_id = ?", (oldcompatibility[2], ))
        data.commit()


# matching_algorithm(109)
    
