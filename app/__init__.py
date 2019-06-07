from flask import Flask, url_for, g, send_from_directory, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app.models import User, Band, Venue, Favorite, Rating
from config import Config, Keys
import os, json, boto3

app = Flask(__name__)
app.static_folder = 'static'
app.config.from_object(Config)
app.config.from_object(Keys)
# heroku = Heroku(app)

S3_BUCKET = os.environ.get('S3_BUCKET')

file_name = request.args.get('file_name')
file_type = request.args.get('file_type')

s3 = boto3.client('s3')


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

@app.route('/sign_s3/')
def sign_s3():
    S3_BUCKET = os.environ.get('S3_BUCKET')

    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')

    s3 = boto3.client('s3')

    presigned_post = s3.generate_presigned_post(
        Bucket = S3_BUCKET,
        Key = file_name,
        Fields = {"acl": "public-read", "Content-Type": file_type},
        Conditions = [
        {"acl": "public-read"},
        {"Content-Type": file_type}
        ],
        ExpiresIn = 3600
    )

    return json.dumps({
        'data': presigned_post,
        'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
    })

@app.route("/submit_form/", methods = ["POST"])
def submit_form():
    avatar_url = request.form["avatar-url"]

    update_account(avatar_url)

    return redirect(url_for('index'))

from app.routes import admin, auth, band, main, user, venue
