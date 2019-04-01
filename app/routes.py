from flask import render_template, url_for
from app import app

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/user") # this will need to be a dynamic route
def user():
    return "User Page Under Construction"

@app.route('/band') # this will need to be a dynamic route
def band():
    return "Band page Under Construction"

@app.route('/venue') # this will need to be a dynamic route
def venue():
    return "Venue page Under Construction"

# @app.route('/404') 
# def venue():
#     return render_template('404.html')
