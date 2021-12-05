import os 
from functools import wraps
from flask import render_template, escape, session, redirect
import urllib.parse

def apology(message):
    return render_template("apology.html", bottom=escape(message)), code

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
    elif len(rows) != 0: 
        return apology("Username already taken.")


# def matching_algorithm():
#     mentees = db.execute("SELECT * FROM mentees")
#     mentors = db.execute("SELECT * FROM mentors")
#     for mentee in mentees: 
#         #Create a temporary table that contains all match scores 
#         db.execute("CREATE TABLE #matches (mentee_id int, mentor_id, match_score float")
#         for mentor in mentors: 
#             #Check that we're only calculating scores for mentors that can take another mentee
#             spots_left = db.execute("SELECT mentee_count FROM mentor")
#             if spots_left > 0:
#                 #Calculate the match score between mentee and mentor
#                 match_score = 0
#                 mentor_id = db.execute("SELECT id FROM mentor")
#                 #insert this score into the temporary table #matches
#                 db.execute("INSERT INTO #matches (mentor_id, match_score) VALUES (?,?)") mentor_id, match_score)
         
#         #Sort the match table from highest to lowest score
#         #Match mentee with mentor with the first row and update final matches table
#         #Decrease the mentee_count for the mentor. 
#         #If there are no mentors, put mentee on waiting list table. 
        

        
