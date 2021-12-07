# qbmentee-matching


Instructions: Documentation for your project in the form of a Markdown file called README.md. This documentation is to be a user’s manual for your project. Though the structure of your documentation is entirely up to you, it should be incredibly clear to the staff how and where, if applicable, to compile, configure, and use your project. Your documentation should be at least several paragraphs in length. It should not be necessary for us to contact you with questions regarding your project after its submission. Hold our hand with this documentation; be sure to answer in your documentation any questions that you think we might have while testing your work.

# SETUP
Download the files and open it up locally in vscode. (We were aiming to get the website hosted publicly on Heroku, but were not able to make it time for the deadline, hence the need to run the project locally). Make sure that you are in the qbmentee-matching directory. You may need to install some libraries if you don't have them already. Run pip3 install [library name] for the libraries you do not have installed: 
    -Flask-Session
    -sqlite3 Type 
    -flask
    -os
    -time
    -jinja2
Now, type into terminal "flask run" and open the port link the application is running on.


# Home Page and Register
The first thing you should see is the homepage. The homepage has general information about the mission of Spark and how the mentorship program works. Click the buttons about learning more about the program and scroll down! At the bottom there is a link to register/make an account. There is also a link to the discord community server that we are basing our project off of. 

Click the register button. Note that as of right now, the database will have many mentors registered and no mentees register because that's what would happen in real life at the start of the Spark matching process. The matching algorithm runs every time a mentee registers so that they can be matched with a mentor automatically + be matched with a mentor they have the most similarity with instead of being matched solely when a mentor becomes available. The user flows for mentors and mentees are generally similar, only with slight differences in the registration process. We will walk you through both! 


# Mentor User Flow
On the registration page, type in your full name, as well as your password, email, and discord name (you don't have to put your real information but please fill out all of the input boxes). Make sure that you have "mentor" selected then click next. You will be directed to survey. YOU MUST ANSWER ALL QUESTIONS ON THE SURVEY! Check of "I agree" for all of the terms and conditions, then select the best options for each background question. Once you're done, submit. Hopefully that entire registration process felt very very easy. We wanted to make it as efficient and comprehensive as possible. 

Now, you will be on your mentor dashboard. There are currently no mentees that you are assigned to. Mentees get matched with mentors based on which mentor they have the highest "match score" with. So as soon as you have a high match score with a mentee, the mentee's profile will appear on your dashboard. 

We will now show you what a "populated" mentor dashboard looks like. Go to the icon on the top left of the page and click logout. Login and enter the following information:
     -Username: Lisber
     -Password: 123456
     -Role: Mentor

Now, you can see a populated dashboard. Lisber has two mentees (Christy and Mia) assigned to her and she will not have any more populate on her dashboard because she indicated on the registration survey that she could take at most 2 mentees. If you click on the more info button on Christy, you can see that Lisber can see a note that Christy wrote in her registration survey as well as other information like her contact info and the top three Questbridge Schools she wants to rank. Currently, we have a "contact" button that is supposed to allow the mentor to send an email to the mentee, but that feature was not able to be fully implemented. The UI is still there for you to see! At the bottom of the dashboard, you'll be able to see a history of meetings the mentor has had/will have with their mentees. 

Next, head to the scheduler tab. In here you can schedule meetings with your mentees. Select the time, date, and insert a meeting link (google meet, zoom ). The meeting information will populate in the main dashboard. 

Next, head to the notetaker tab. Here, you can write notes that will sync with your mentees. You can also delete the notes.  

Next, head to the Resources tab. This is just a page with a few resources that alumni have found helpful when navgiating the college application process. Mentors and mentees both have access to these resources! 


# Mentee User Flow
Navigate to the registration page by going to Spark home. You are now going to register as a mentee! On the registration page, type in the information of a hypothetical mentee. Make sure that you have "mentee" selected then click next. You will be directed to survey. YOU MUST ANSWER ALL QUESTIONS ON THE SURVEY! Check of "I agree" for all of the terms and conditions, then select the best options for each background question. Notice how the mentee survey is slightly more involved. Mentees get to submit ranking preferences for which identity aspects they think are most important to have in a mentor. The algorithm takes these rankings and adjusts weights accordingly when calculating match scores. For example, if you weight academic pathway as a 1, the algorithm will place the highest weight on that category when finding you a mentor! Additionally, mentees fill out logistics questions about their timezone and the questbridge schools they intend on ranking. The final text box is for the mentee to write anything they'd want their mentor to know. This will appear on the mentor's dashboard. 

Once you're done, submit. You can see that the mentee dashboard is very similar to the mentor dashboard. And, you can find that you have been matched to a mentor! The matching algorithm gets run immediately after a mentee registers. If in the case that there are not enough mentors, the mentee will be placed on a waitlist.








