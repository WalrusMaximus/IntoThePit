from flask import render_template, url_for
from app import app
from app.forms import LoginForm, RegisterForm

@app.route("/")
def index():
    form = RegisterForm()
    return render_template('layout.html', title="Into The Pit", form=form)

@app.route("/user") # this will need to be a dynamic route
def user():
    return "User Page Under Construction"

@app.route('/band') # this will need to be a dynamic route
def band():
    return "Band page Under Construction"

@app.route('/venue') # this will need to be a dynamic route
def venue():
    return "Venue page Under Construction"

@app.route('/register')
def register():
    form = RegisterForm()
    return render_template('register.html', title='Into The Pit - Register', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title="Into The Pit - Login", form=form)



# @app.route('/404') 
# def venue():
#     return render_template('404.html')
