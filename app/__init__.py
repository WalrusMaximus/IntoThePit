from flask import Flask, url_for, g, send_from_directory, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app.models import User, Band, Venue, Favorite, Rating
from config import Config, Keys
import cloudinary as Cloud
import os

app = Flask(__name__)
app.static_folder = 'static'
app.config.from_object(Config)
app.config.from_object(Keys)

if os.environ['ENV'] == 'prod':
    SONGKICK_KEY = os.environ.get('SONGKICK_KEY')
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
else:
    SONGKICK_KEY = Keys.SONGKICK_API_KEY
    CLOUDINARY_API_SECRET = Keys.CLOUDINARY_API_SECRET
    CLOUDINARY_API_KEY = Keys.CLOUDINARY_API_KEY
    CLOUDINARY_CLOUD_NAME = Keys.CLOUDINARY_CLOUD_NAME

Cloud.config.update = ({
    'cloud_name':CLOUDINARY_CLOUD_NAME,
    'api_key':CLOUDINARY_API_KEY,
    'api_secret':CLOUDINARY_API_SECRET
})
# 

from app.models import DATABASE

# Create production/development conditional CHECK
# add cloudinary functionality
# add email confirmation
# add password forget function
# add password change function
# update database to include user confirmation, user creation date 

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

@app.route("/submit_form/", methods = ["POST"])
def submit_form():
    avatar_url = request.form["avatar-url"]

    update_account(avatar_url)

    return redirect(url_for('index'))

from app.routes import admin, auth, band, main, user, venue
