from flask import render_template
from app import app, models

@app.route("/", methods=["POST","GET"])
def index():
    venues = models.Venue.select().order_by(models.Venue.name)
    bands = models.Band.select().order_by(models.Band.name)
    return render_template('index.html', title="Into The Pit", venues=venues, bands=bands)