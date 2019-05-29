from flask import render_template, url_for, flash, redirect
from app import app, models, forms
from flask_login import current_user, login_required

@app.route('/venue/add_favorite/<id>')
@login_required
def add_favorite_venue(id):
    venue = models.Venue.get(models.Venue.id == id)
    if models.Favorite.select().where(
        (models.Favorite.venue_fk == venue.id) &
        (models.Favorite.user_fk == current_user.id)):
            flash("Can't add a venue to your favorites twice","error")
            return redirect(url_for('venue',id=id))
    else:
        flash(f"Added {venue.name} to your favorites!","success")
        models.Favorite.create_favorite(
            user_fk=current_user.id,
            venue_fk=venue
        )
        return redirect(url_for('venue',id=id))

@app.route('/venue/delete_favorite/<id>')
@login_required
def delete_favorite_venue(id):
    venue = models.Venue.get(models.Venue.id == id)
    favorite = models.Favorite.select().where(
        (models.Favorite.venue_fk == venue.id) &
        (models.Favorite.user_fk == current_user.id))
    if favorite.exists():
        delete_favorite = models.Favorite.delete().where(
        (models.Favorite.venue_fk == venue.id) &
        (models.Favorite.user_fk == current_user.id))
        delete_favorite.execute()
        flash("Deleted from favorites","success")
        return redirect(url_for('venue',id=id))
    else:
        flash("This isn't one of your favorite venues","error")
        models.Favorite.create_favorite(
            user_fk=current_user.id,
            venue_fk=venue
        )
        return redirect(url_for('venue',id=id))
        

@app.route('/venue/<id>', methods=('GET', 'POST'))
def venue(id):
    venue = models.Venue.get(models.Venue.id == id)
    ratings = models.Rating.select().where(models.Rating.venue_fk == venue.id)
    form = forms.RatingForm()
    venueskid = venue.skid
    bands_to_approve = models.Band.select()
    approved_bands = []

    for bands in bands_to_approve:
        approved_bands.append(bands.skid)

    overall_rating = 0
    overall_num = 0
    pit_rating = 0
    pit_num = 0
    sound_rating = 0
    sound_num = 0
    facility_rating = 0
    facility_num = 0

    for rating in ratings:
        if rating.rating_type == "Overall":
            overall_rating = overall_rating + int(rating.rating)
            overall_num = overall_num + 1
        if rating.rating_type == "Mosh Pit":
            pit_rating = pit_rating + int(rating.rating)
            pit_num = pit_num + 1
        if rating.rating_type == "Sound":
            sound_rating = sound_rating + int(rating.rating)
            sound_num = sound_num + 1
        if rating.rating_type == "Facilities":
            facility_rating = facility_rating + int(rating.rating)
            facility_num = facility_num + 1

    if overall_num == 0:
        overall_rating = "N/A"
    else: 
        overall_rating = overall_rating / overall_num
        overall_rating = round(overall_rating, 1)
    if pit_num == 0:
        pit_rating = "N/A"
    else: 
        pit_rating = pit_rating / pit_num
        pit_rating = round(pit_rating, 1)
    if sound_num == 0:
        sound_rating = "N/A"
    else: 
        sound_rating = sound_rating / sound_num
        sound_rating = round(sound_rating, 1)
    if facility_num == 0:
        facility_rating = "N/A"
    else: 
        facility_rating = facility_rating / facility_num
        facility_rating = round(facility_rating, 1)

    is_favorite = False

    if current_user.is_anonymous == False:

        if models.Favorite.select().where(
            (models.Favorite.user_fk == current_user.id) &
            (models.Favorite.venue_fk == venue.id)
        ):
            is_favorite = True

    if form.validate_on_submit():
        locator = models.Rating.select().where(
            (models.Rating.venue_fk == venue.id) &
            (models.Rating.user_fk == current_user.id) &
            (models.Rating.rating_type == form.rating_type.data))
        if locator.count() == 0:
            flash(f"Add comment to {venue.name}.")
            models.Rating.create_rating(
                user_fk=current_user.id,
                venue_fk=id,
                rating=form.rating.data,
                rating_type=form.rating_type.data,
                message=form.message.data
            )
            return redirect(url_for('venue', id=venue.id))
        else:
            flash(f"You can only add one comment per category on each venue")
            return redirect(url_for('venue', id=venue.id))
    return render_template('venue.html', venue=venue, approved_bands=approved_bands, ratings=ratings, form=form, id=id, is_favorite=is_favorite, venueskid=venueskid, overall_rating=overall_rating, pit_rating=pit_rating, sound_rating=sound_rating, facility_rating=facility_rating)
    
@app.route('/venue/update_rating/<id>', methods=('GET', 'POST'))
def venue_update_rating(id):
    rating = models.Rating.get(models.Rating.id == id)
    venue = models.Venue.get(models.Venue.id == rating.venue_fk.id)
    ratings = models.Rating.select().where(models.Rating.venue_fk == venue.id)
    record = models.Rating.select().where(id == models.Rating.id).dicts().get()
    venueskid = venue.skid

    overall_rating = 0
    overall_num = 0
    pit_rating = 0
    pit_num = 0
    sound_rating = 0
    sound_num = 0
    facility_rating = 0
    facility_num = 0

    for rating in ratings:
        if rating.rating_type == "Overall":
            overall_rating = overall_rating + int(rating.rating)
            overall_num = overall_num + 1
        if rating.rating_type == "Mosh Pit":
            pit_rating = pit_rating + int(rating.rating)
            pit_num = pit_num + 1
        if rating.rating_type == "Sound":
            sound_rating = sound_rating + int(rating.rating)
            sound_num = sound_num + 1
        if rating.rating_type == "Facilities":
            facility_rating = facility_rating + int(rating.rating)
            facility_num = facility_num + 1

    if overall_num == 0:
        overall_rating = "N/A"
    else: 
        overall_rating = overall_rating / overall_num
        overall_rating = round(overall_rating, 1)
    if pit_num == 0:
        pit_rating = "N/A"
    else: 
        pit_rating = pit_rating / pit_num
        pit_rating = round(pit_rating, 1)
    if sound_num == 0:
        sound_rating = "N/A"
    else: 
        sound_rating = sound_rating / sound_num
        sound_rating = round(sound_rating, 1)
    if facility_num == 0:
        facility_rating = "N/A"
    else: 
        facility_rating = facility_rating / facility_num
        facility_rating = round(facility_rating, 1)

    is_favorite = False

    if current_user.is_anonymous == False:

        if models.Favorite.select().where(
            (models.Favorite.user_fk == current_user.id) &
            (models.Favorite.venue_fk == venue.id)
        ):
            is_favorite = True

    form = forms.RatingForm()
    ratings = models.Rating.select().where(models.Rating.venue_fk == venue.id)
    if form.validate_on_submit():
        rating_update = models.Rating.update(
            rating=form.rating.data,
            message=form.message.data
        ).where(models.Rating.id == id)
        rating_update.execute()
        flash(f"Updated comment on {rating.venue_fk.name}.")
        return redirect(url_for('venue',id=venue.id))
    return render_template('venue.html', venue=venue, rating=rating, is_favorite=is_favorite, ratings=ratings, form=form, record=record, venueskid=venueskid, overall_rating=overall_rating, pit_rating=pit_rating, sound_rating=sound_rating, facility_rating=facility_rating)

