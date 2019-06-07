from flask import Flask, url_for, g, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app.models import User, Band, Venue, Favorite, Rating
from config import Config, Keys
import os

app = Flask(__name__)
app.static_folder = 'static'
app.config.from_object(Config)
app.config.from_object(Keys)
# heroku = Heroku(app)

SONGKICK_KEY = Keys.SONGKICK_API_KEY

from app.models import DATABASE

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return User.get(User.id == userid)
    except:
        return None;

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

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

from app.routes import admin, auth, band, main, user, venue
