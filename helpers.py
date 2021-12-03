# import os 
# from functools import wraps
# from flask import g, request, redirect, url_for, session
# # import requests
# import urllib.parse

# def login_required(f):
#     """
#     Check to see if a user is logged in or not.
#     Will redirect user to login page if they are not a user 
#     https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
#     """

#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if session.get("user_id") is None:
#             return redirect("/login")
#         return f(*args, **kwargs)
#     return decorated_function

