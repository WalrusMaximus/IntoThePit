from flask import render_template, request, redirect
from app import app, models, forms

@app.route("/", methods=["POST","GET"])
def index():
    venue_check = models.Venue.select()
    band_check = models.Band.select()
    no_venues = ""
    no_bands = ""
    if venue_check.exists():
        venues = models.Venue.select().order_by(models.Venue.name)
    else:
        venues = None
        no_venues = "none"
    if band_check.exists():
        bands = models.Band.select().order_by(models.Band.name)
    else:
        bands = None
        no_bands = "none"

    form = forms.SearchForm()

    term = False

    if request.method == 'POST':
        if form.validate_on_submit():
            term = form.search.data
            venues = []
            bands = []
            for venue in venue_check:
                print(venue)
                if term.lower() in venue.display_name.lower():
                    venues.append(venue)
            for band in band_check:
                if term.lower() in band.display_name.lower():
                    bands.append(band)
            if len(venues) == 0:
                no_venues = "search_fail"
            if len(bands) == 0:
                no_bands = "search_fail"
                print(no_bands)

    return render_template('index.html',
        title="Into The Pit",
        form=form,
        venues=venues,
        bands=bands,
        no_bands=no_bands,
        no_venues=no_venues,
        search_term=term
    )

