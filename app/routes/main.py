from flask import render_template
from app import app, models

@app.route("/", methods=["POST","GET"])
def index():
    venue_check = models.Venue.select()
    band_check = models.Band.select()
    no_venues = False
    no_bands = False
    if venue_check.exists():
        venues = models.Venue.select().order_by(models.Venue.name)
    else:
        venues = None
        no_venues = True
    if band_check.exists():
        bands = models.Band.select().order_by(models.Band.name)
    else:
        bands = None
        no_bands = True
    return render_template('index.html', title="Into The Pit", venues=venues, bands=bands, no_bands=no_bands, no_venues=no_venues)