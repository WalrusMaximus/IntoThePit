from flask import Flask, url_for
from app.models import User, Band, Venue, FavBand, Rating, Friend, Event

app = Flask(__name__)
app.static_folder = 'static'
app.config['SECRET_KEY'] = "beepboopiamrobotbeepboop"

from app import routes
