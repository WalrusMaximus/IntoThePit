from flask import render_template, url_for, flash, redirect, request
from app import app, models, forms
from app.functions import user_img
from flask_login import current_user, login_required
import cloudinary, cloudinary.uploader, cloudinary.api
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

@app.route("/user/<id>")
def user(id):
    user = models.User.get(models.User.id == id)
    ratings = models.Rating.select().where(models.Rating.user_fk == user.id)
    show_ratings = True

    try:
        image_query = cloudinary.api.resource(f"user/{user.username}")
        avatar = image_query['url']
    except:
        avatar = False

    favorites = models.Favorite.select().where(models.Favorite.user_fk == id)
    favorite_bands = []
    favorite_venues = []

    for band in favorites:
        if band.band_fk:
            favorite_bands.append(band)

    for venue in favorites:
        if venue.venue_fk:
            favorite_venues.append(venue)


    bands_query = []
    venues_query = []

    bands_to_approve = models.Band.select()
    approved_bands = []

    for bands in bands_to_approve:
        approved_bands.append(bands.skid)

    for favorite in favorite_bands:
        if favorite.band_fk.skid:
            bands_query.append(favorite.band_fk.skid)

    for favorite in favorite_venues:
        if favorite.venue_fk.skid:
            venues_query.append(favorite.venue_fk.skid)

    return render_template(
        'user.html',
        user=user,
        ratings=ratings,
        favorite_bands=favorite_bands,
        favorite_venues=favorite_venues,
        show_ratings=show_ratings,
        bands_query=bands_query,
        venues_query=venues_query,
        approved_bands=approved_bands,
        avatar=avatar,
    )

@app.route('/user/update_rating/<id>', methods=['GET','POST'])
@login_required
def user_update_rating(id):
    user = models.User.get(models.User.id == current_user.id)
    ratings = models.Rating.select().where(models.Rating.user_fk == user.id)
    show_ratings = True
    no_favorites = True

    form = forms.RatingForm()
    rating = models.Rating.get(models.Rating.id == id)
    ratings = models.Rating.select().where(models.Rating.user_fk == user.id)
    record = models.Rating.select().where(id == models.Rating.id).dicts().get()
    if form.validate_on_submit():
        rating_update = models.Rating.update(
            rating=form.rating.data,
            message=form.message.data
        ).where(models.Rating.id == id)
        rating_update.execute()
        flash(f"Updated comment on {rating.venue_fk.name}.","success")
        return redirect(url_for('user',id=current_user.id))

    return render_template(
        'user.html',
        user=user,
        form=form,
        record=record,
        rating=rating,
        ratings=ratings,
        show_ratings=show_ratings,
        no_favorites=no_favorites
    )

@app.route("/user/update_img/<id>", methods=["POST","GET"])
def update_user(id):
    user = models.User.get(models.User.id == id)
    ratings = models.Rating.select().where(models.Rating.user_fk == user.id)
    form = forms.UpdateUserForm()
    img_updating = True
    show_ratings = True

    try:
        image_query = cloudinary.api.resource(f"user/{user.username}")
        avatar = image_query['url']
    except:
        avatar = False

    favorites = models.Favorite.select().where(models.Favorite.user_fk == id)
    favorite_bands = []
    favorite_venues = []

    for band in favorites:
        if band.band_fk:
            favorite_bands.append(band)

    for venue in favorites:
        if venue.venue_fk:
            favorite_venues.append(venue)

    bands_query = []
    venues_query = []

    bands_to_approve = models.Band.select()
    approved_bands = []

    for bands in bands_to_approve:
        approved_bands.append(bands.skid)

    for favorite in favorite_bands:
        if favorite.band_fk.skid:
            bands_query.append(favorite.band_fk.skid)

    for favorite in favorite_venues:
        if favorite.venue_fk.skid:
            venues_query.append(favorite.venue_fk.skid)
        

    if form.validate_on_submit():
        img = form.avatar.data
        try:
            uploading = upload(img, overwrite=True, version=1, public_id=user.username, folder='user', format="png", width=256, height=255, crops="fill")
            image_query = cloudinary.api.resource(f"user/{user.username}")
            avatar = image_query['url']
            user_update = models.User.update(
                avatar=avatar
            ).where(models.User.id == id)
            user_update.execute()
            flash(f"Image for {user.username} updated","success")
        except:
            flash(f"Couldn't connect to server.. try again.","error")
        return redirect(url_for('user',id=id))
        
    return render_template(
        'user.html',
        user=user,
        form=form,
        img_updating=img_updating,
        ratings=ratings,
        favorite_bands=favorite_bands,
        favorite_venues=favorite_venues,
        show_ratings=show_ratings,
        bands_query=bands_query,
        venues_query=venues_query,
        approved_bands=approved_bands,
        avatar=avatar
    )

    # ########## COMMENTS ########## #

@app.route('/user/delete_rating/<id>', methods=('GET', 'POST'))
def delete_rating(id):
    profile = request.args.get('profile')
    rating = models.Rating.get(models.Rating.id == id)
    if rating.user_fk.id == current_user.id:
        rating_deletion = models.Rating.delete().where(models.Rating.id == rating.id)
        rating_deletion.execute()
        flash(f"Deleted rating on {rating.venue_fk.name}")
        if profile == "True":
            return redirect(url_for('user', id=current_user.id))
        return redirect(url_for('venue', id=rating.venue_fk.id))
    else:
        flash(f"You cannot delete another users comments","error")
        return redirect(url_for('index'))