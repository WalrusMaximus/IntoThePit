from flask import Flask, url_for, g, send_from_directory, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app.models import User, Band, Venue, Favorite, Rating
from app.config import Keys
import cloudinary
import os

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = os.environ.get('SECRET_KEY')
app.config['SONGKICK_API_KEY'] = os.environ.get('SONGKICK_API_KEY')

cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
)



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

from app.routes import admin, auth, band, main, user, venue
