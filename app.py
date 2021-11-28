from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)

# List of QB schools b/c listing them in survey would be too long and also QB schools have big potential to change
schools = ["Amherst College", "Barnard College", "Boston College", "Boston University", "Bowdoin College","Brown University",
"California Institute of Technology","Carleton College","Claremont McKenna College","Colby College","Colgate University",
"Colorado College","Columbia University","Dartmouth College","Davidson College","Denison University","Duke University","Emory University",
"Grinnell College","Hamilton College","Haverford College","Macalester College","Massachusetts Institute of Technology","Northwestern University",
"Oberlin College","Pomona College","Princeton University","Rice University","Scripps College","Stanford University","Swarthmore College",
"Tufts University","University of Chicago","University of Notre Dame","University of Pennsylvania","University of Southern California",
"University of Virginia","Vanderbilt University","Vassar College","Washington and Lee University","Washington University in St. Louis",
"Wellesley College","Wesleyan University","Williams College","Yale University"]

@app.route('/')
def hello():
    return "Hello World hi QB mentee matching!"

@app.route('/menteeresgistration', methods=["GET", "POST"])
def hello():
    if request.method == "GET":
        return render_template("menteeregistration.html")

#making sure to pass on the list of schools to the html for the mentees and mentors surveys
@app.route('/menteesurvey', methods=["GET", "POST"])
def hello():
    if request.method == "GET":
        return render_template("menteesurvey.html", schools=schools)

@app.route('/mentorsurvey', methods=["GET", "POST"])
def hello():
    if request.method == "GET":
        return render_template("mentorsurvey.html", schools=schools)

