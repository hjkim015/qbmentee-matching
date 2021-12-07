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
    #Select all available mentors
    cmentors = db.execute("SELECT person_id FROM mentee_count WHERE mentees_left > 0").fetchall()
    print(cmentors)
    mentor_count = int(len(cmentors))

    # Compatibitility trackers store match score, mentee_id, and mentor_id
    oldcompatibility = [0,0,0]
    # newcompatibility = [0,0,0]
    mentee_id = str(mentee_id)

    print("start", oldcompatibility[0], oldcompatibility[1], oldcompatibility[2])

    # Store mentee's category weights 
    academics = db.execute("SELECT academics FROM rankings WHERE person_id = ?", (mentee_id, )).fetchall()[0][0]
    gender = db.execute("SELECT gender FROM rankings WHERE person_id = ?", (mentee_id, )).fetchall()[0][0]
    religion = db.execute("SELECT religion FROM rankings WHERE person_id = ?", (mentee_id, )).fetchall()[0][0]
    ethnicity = db.execute("SELECT ethnicity FROM rankings WHERE person_id = ?", (mentee_id, )).fetchall()[0][0]
    citizenship = db.execute("SELECT citzenship FROM rankings WHERE person_id = ?", (mentee_id, )).fetchall()[0][0]

    for mentor in cmentors: 
        print("mentor_id, mentee_id", mentor[0], mentee_id)
        mentor = str(mentor[0])
        #If that mentor can take on more mentees
        if mentor_count > 0:
            match_score = 0
            #Calcuate academics match
            academicsmatch1 = db.execute("SELECT academic_pathway FROM academics WHERE person_id = ?", (mentee_id,)).fetchall()[0]
            academicsmatch2 = db.execute("SELECT academic_pathway FROM academics WHERE person_id = ?", (mentor, )).fetchall()[0]

            if academicsmatch1 == academicsmatch2:
                academicsmatch = 1
                match_score = match_score + academics
                        
            #Calculate Gender match
            gendermatch1 = db.execute("SELECT gender FROM gender WHERE person_id = ?", (mentee_id, )).fetchall()[0]
            gendermatch2 = db.execute("SELECT gender FROM gender WHERE person_id = ?", (mentor, )).fetchall()[0]
            if gendermatch1 == gendermatch2:
                match_score = match_score + gender

            #Calculate Religion Match
            religionmatch1 = db.execute("SELECT religion FROM religion WHERE person_id = ?", (mentee_id,)).fetchall()[0]
            print(religionmatch1)
            religionmatch2 = db.execute("SELECT religion FROM religion WHERE person_id = ?", (mentor,)).fetchall()[0]
            print(religionmatch2)
            if religionmatch1 == religionmatch2:
                print("match_score, religion", match_score, religion)
                match_score = match_score + religion
            

            #Calculate Citizenship Match
            citizenshipmatch1 = db.execute("SELECT citizenship FROM citizenship WHERE person_id = ?", (mentee_id, )).fetchall()[0]
            citizenshipmatch2 = db.execute("SELECT citizenship FROM citizenship WHERE person_id = ?", (mentor, )).fetchall()[0]
            if citizenshipmatch1 == citizenshipmatch2:
                citizenshipmatch = 1
                match_score = match_score + citizenship

            # Calculate Ethnicity Match 
            ethnicitymatch1 = db.execute("SELECT ethnicity FROM ethnicity WHERE person_id = ?", (mentee_id, )).fetchall()[0]
            ethnicitymatch2 = db.execute("SELECT ethnicity FROM ethnicity WHERE person_id = ?", (mentor, )).fetchall()[0]
            if ethnicitymatch1 == ethnicitymatch2:
                match_score = match_score + ethnicity
           
            # ethnicitymatch1 = db.execute("SELECT COUNT(black) FROM ethnicity WHERE person_id = ? OR person_id = ?", (mentee_id, mentor, )) + 1
            # ethnicitymatch2 = db.execute("SELECT COUNT(asian) FROM ethnicity WHERE person_id = ?) = (SELECT asian FROM ethnicity WHERE person_id = ?))", (mentee_id, mentor, )) + 1
            # ethnicitymatch3 = db.execute("SELECT COUNT(american_india) FROM ethnicity WHERE person_id = ? OR person_id = ?", (mentee_id, mentor, )) + 1
            # ethnicitymatch4 = db.execute("SELECT COUNT(pacific_islander) FROM ethnicity WHERE person_id = ? OR person_id = ?", (mentee_id, mentor, )) + 1
            # ethnicitymatch5 = db.execute("SELECT COUNT(white) FROM ethnicity WHERE person_id = ? OR person_id = ?", (mentee_id, mentor, )) + 1
            # ethnicitymatch6 = db.execute("SELECT COUNT(latinx) FROM ethnicity WHERE person_id = ? OR person_id = ?", (mentee_id, mentor, )) + 1
            # ethnicitymatch7 = db.execute("SELECT COUNT(none) FROM ethnicity WHERE person_id = ? OR person_id = ?", (mentee_id, mentor, )) + 1
            # ethnicitymatch = (ethnicitymatch1%2 + ethnicitymatch2%2 + ethnicitymatch3%2 + ethnicitymatch4%2 + ethnicitymatch5%2 + ethnicitymatch6%2 + ethnicitymatch7%2)/7
           
            #Calculate the Overall Match Score 
            # match_score = (academics * academicsmatch)[0] + (religion * religionmatch)[0] + (citizenship * citizenshipmatch)[0] + (gender * gendermatch)[0] + (ethnicity * ethnicitymatch)[0]
            # print((academics * academicsmatch])
           
            #If the current Match Score is higher than the previous match score:
            #Replace the old compatibility score with the current match score
            # print("match_score", match_score)
            # print("oldcompatibility[0]", oldcompatibility[0])
            if match_score > oldcompatibility[0] or match_score == oldcompatibility[0]: 
                oldcompatibility[0] = match_score
                oldcompatibility[1] = mentee_id
                oldcompatibility[2] = mentor
        else:
            #Put the student on the waitlist -> 0 for mentor_id
            db.execute("INSERT INTO matches (score, mentee_id, mentor_id) VALUES (?,?,?)", (0, mentee_id, 0))
 
    #After going through all mentors, highest match score stored in old compatiability score
    #Push to matches the old compatability information
    db.execute("INSERT INTO matches (score, mentee_id, mentor_id) VALUES (?,?,?)", (oldcompatibility[0], oldcompatibility[1], oldcompatibility[2], ))    
    print("final thing to push to matches", oldcompatibility[0], oldcompatibility[1], oldcompatibility[2])

    #Decrease the number of mentees the mentor can take on by 1.
    db.execute("UPDATE mentee_count SET mentees_left = mentees_left - 1 WHERE person_id = ?", (oldcompatibility[2], ))
    data.commit()

# matching_algorithm(4)
    
