from flask import Flask, url_for, g
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app.models import User, Band, Venue, Favorite, Rating, Friend, Event
from config import Config

app = Flask(__name__)
app.static_folder = 'static'
app.config.from_object(Config)

from app.models import DATABASE

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return User.get(User.id == userid)
    except DoesNotExist:
        return None

# Connect to database before request
@app.before_request
def before_request():
    g.db = DATABASE
    g.db.connect()
    g.user = current_user

# Close database after request
@app.after_request
def after_request(response):
    g.db.close()
    return response

from app import routes
