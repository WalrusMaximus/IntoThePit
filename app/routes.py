from flask import render_template, url_for, flash, redirect, g, request
import os
from PIL import Image
from app import app, models
from app.forms import LoginForm, RegisterForm, AddUserForm, UpdateUserForm, VenueForm, BandForm, RatingForm, AdminUpdateUserForm, UpdateRatingForm, ImgForm
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# FUNCTIONS

def user_img(form_picture, user_name):
    _, f_ext = os.path.splitext(form_picture.filename)
    file_path = "images/user_"
    picture_save = file_path + user_name + f_ext
    picture_path = os.path.join(app.root_path, 'static', picture_save)
    output_size = (512, 512)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_save

def venue_img(form_picture, venue_name):
    _, f_ext = os.path.splitext(form_picture.filename)
    file_path = "images/venue_"
    picture_save = file_path + venue_name.lower().replace(" ", "_") + f_ext
    picture_path = os.path.join(app.root_path, 'static', picture_save)
    output_size = (512, 512)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_save

def band_img(form_picture, band_name):
    _, f_ext = os.path.splitext(form_picture.filename)
    file_path = "images/band_"
    picture_save = file_path + band_name.lower().replace(" ", "_") + f_ext
    picture_path = os.path.join(app.root_path, 'static', picture_save)
    output_size = (512, 512)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_save

    # ########## MAIN PAGE ########## #

@app.route("/", methods=["POST","GET"])
def index():
    venues = models.Venue.select()
    bands = models.Band.select()
    return render_template('index.html', title="Into The Pit", venues=venues, bands=bands)

    # ########## LOGIN ########## #

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash(f"Registered { form.email.data }", 'success')
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()

    if current_user.is_anonymous == False:
        return redirect(url_for('user',id=current_user.id))

    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("your email or password doesn't match", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in", "success")
                return redirect(url_for('index'))
            else:
                flash("your email or password doesn't match", "error")
    return render_template('login.html', form=form)

    # ########## USER PAGES ########## #

@app.route("/user/<id>")
def user(id):
    user = models.User.get(models.User.id == id)
    ratings = models.Rating.select().where(models.Rating.user_fk == user.id)
    show_ratings = True

    favorite_bands = models.Favorite.select().where(
        (models.Favorite.user_fk == id) &
        (models.Favorite.band_fk))
    favorite_venues = models.Favorite.select().where(
        (models.Favorite.user_fk == id) &
        (models.Favorite.venue_fk))

    bands_query = []
    venues_query = []

    bands_to_approve = models.Band.select()
    approved_bands = []

    for bands in bands_to_approve:
        approved_bands.append(bands.skid)

    if favorite_bands:
        for favorite in favorite_bands:
            bands_query.append(favorite.band_fk.skid)

    if favorite_venues:
        for favorite in favorite_venues:
            venues_query.append(favorite.venue_fk.skid)
        

    return render_template('user.html', user=user, ratings=ratings, favorite_bands=favorite_bands, favorite_venues=favorite_venues, show_ratings=show_ratings, bands_query=bands_query, venues_query=venues_query, approved_bands=approved_bands)


@app.route('/user/update_rating/<id>', methods=['GET','POST'])
@login_required
def user_update_rating(id):
    user = models.User.get(models.User.id == current_user.id)
    ratings = models.Rating.select().where(models.Rating.user_fk == user.id)
    show_ratings = True
    no_favorites = True

    form = UpdateRatingForm()
    rating = models.Rating.get(models.Rating.id == id)
    ratings = models.Rating.select().where(models.Rating.user_fk == user.id)
    record = models.Rating.select().where(id == models.Rating.id).dicts().get()
    if form.validate_on_submit():
        rating_update = models.Rating.update(
            rating=form.rating.data,
            message=form.message.data
        ).where(models.Rating.id == id)
        rating_update.execute()
        flash(f"Updated comment on {rating.venue_fk.name}.")
        return redirect(url_for('user',id=current_user.id))

    return render_template('user.html', user=user, form=form, record=record, rating=rating, ratings=ratings, show_ratings=show_ratings, no_favorites=no_favorites)

@app.route("/user/update_img/<id>", methods=["POST","GET"])
def update_user(id):
    user = models.User.get(models.User.id == id)
    ratings = models.Rating.select().where(models.Rating.user_fk == user.id)
    form = UpdateUserForm()
    img_updating = True
    show_ratings = True

    favorite_bands = models.Favorite.select().where(
        (models.Favorite.user_fk == id) &
        (models.Favorite.band_fk))
    favorite_venues = models.Favorite.select().where(
        (models.Favorite.user_fk == id) &
        (models.Favorite.venue_fk))

    bands_query = []
    venues_query = []

    bands_to_approve = models.Band.select()
    approved_bands = []

    for bands in bands_to_approve:
        approved_bands.append(bands.skid)

    if favorite_bands:
        for favorite in favorite_bands:
            bands_query.append(favorite.band_fk.skid)

    if favorite_venues:
        for favorite in favorite_venues:
            venues_query.append(favorite.venue_fk.skid)

    if form.validate_on_submit():
        # breakpoint()
        # print(form.avatar.data.filename)
        avatar = user_img(form.avatar.data, user.username)
        user_update = models.User.update(
            avatar=user_img(form.avatar.data, user.username)
        ).where(models.User.id == id)
        user_update.execute()
        flash(f"Updated your profile information.")
        return redirect(url_for('user',id=id))
        
    return render_template('user.html', user=user, form=form, img_updating=img_updating, ratings=ratings, favorite_bands=favorite_bands, favorite_venues=favorite_venues, show_ratings=show_ratings, bands_query=bands_query, venues_query=venues_query, approved_bands=approved_bands)

# FAVORITES

@app.route('/band/add_favorite/<id>')
@login_required
def add_favorite_band(id):
    band = models.Band.get(models.Band.id == id)
    if models.Favorite.select().where(
        (models.Favorite.band_fk == band.id) &
        (models.Favorite.user_fk == current_user.id)):
            flash("Can't add a band to your favorites twice","error")
            return redirect(url_for('band',id=id))
    else:
        flash(f"Added {band.name} to your favorites!","success")
        models.Favorite.create_favorite(
            user_fk=current_user.id,
            band_fk=band
        )
        return redirect(url_for('band',id=id))
    
@app.route('/band/delete_favorite/<id>')
@login_required
def delete_favorite_band(id):
    band = models.Band.get(models.Band.id == id)
    favorite = models.Favorite.select().where(
        (models.Favorite.band_fk == band.id) &
        (models.Favorite.user_fk == current_user.id))
    if favorite.exists():
        delete_favorite = models.Favorite.delete().where(
        (models.Favorite.band_fk == band.id) &
        (models.Favorite.user_fk == current_user.id))
        delete_favorite.execute()
        flash("Deleted from favorites","success")
        return redirect(url_for('band',id=id))
    else:
        flash("This isn't one of your favorite bands","error")
        models.Favorite.create_favorite(
            user_fk=current_user.id,
            band_fk=band
        )
        return redirect(url_for('band',id=id))

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
        

@app.route('/band/<id>')
def band(id):
    band = models.Band.get(models.Band.id == id)
    bandskid = band.skid

    is_favorite = False

    if current_user.is_anonymous == False:

        if models.Favorite.select().where(
            (models.Favorite.user_fk == current_user.id) &
            (models.Favorite.band_fk == band.id)
        ):
            is_favorite = True
    
    return render_template('band.html', band=band, is_favorite=is_favorite, bandskid=bandskid)

@app.route('/venue/<id>', methods=('GET', 'POST'))
def venue(id):
    venue = models.Venue.get(models.Venue.id == id)
    ratings = models.Rating.select().where(models.Rating.venue_fk == venue.id)
    form = RatingForm()
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

    form = UpdateRatingForm()
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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out", "success")
    return redirect(url_for('index'))


    # ########## ADMIN & MANAGEMENT ########## #

# ########## USERS ########## #

@app.route('/admin')
@login_required
def admin():
    if current_user.user_level != "walrus":
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))
    
    users = models.User.select()
    venues = models.Venue.select()
    bands = models.Band.select()

    return render_template('admin.html', users=users, venues=venues, bands=bands)

@app.route('/admin/add_user', methods=('GET', 'POST'))
@login_required
def add_user():
    form = AddUserForm()
    users = models.User.select()
    if current_user.user_level != "walrus":
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        flash(f"Created user - { form.email.data }", 'success')
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            user_level=form.user_level.data,
            password=form.password.data
        )
        return redirect(url_for('add_user'))
    return render_template('admin_with_form.html', form=form, users=users)

@app.route('/admin/user/update/<id>', methods=['GET','POST'])
@login_required
def admin_update_user(id):
    form = AdminUpdateUserForm()
    users = models.User.select()
    user = models.User.get(models.User.id == id)

    if current_user.user_level != "walrus":
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user_update = models.User.update(
            user_level=form.user_level.data,
        ).where(models.User.id == id)
        user_update.execute()
        flash(f"Updated information for {user.email}.")
        return redirect(url_for('admin'))

    return render_template('admin_with_form.html', form=form, users=users, user=user)

@app.route('/user/delete/<id>')
@login_required
def delete_user(id):
    user = models.User.get(models.User.id == id)
    if g.user.user_level == "walrus":
        if g.user == user:
            flash("We don't condone seppuku here, get someone else to kill your account","error")
            return redirect(url_for('admin'))
        else:
            user_deletion = models.User.delete().where(models.User.id == user.id)
            user_deletion.execute()
            ratings_deletion = models.Rating.delete().where(models.Rating.venue_fk == user.id)
            ratings_deletion.execute()
            flash(f"Deleted {user.username}")
            return redirect(url_for('admin'))
    else: 
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))
        
# ########## VENUES ########## #

@app.route('/admin/add_venue', methods=('GET', 'POST'))
@login_required
def add_venue():
    form = VenueForm()
    venues = models.Venue.select()
    if current_user.user_level != "walrus":
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        flash(f"Created venue - { form.name.data }", 'success')
        models.Venue.create_venue(
            name=form.name.data,
            about=form.about.data,
            skid=form.skid.data
        )
        return redirect(url_for('add_venue'))
    return render_template('admin_with_form.html', form=form, venues=venues)

@app.route('/admin/venue_img/<id>', methods=('GET','POST'))
@login_required
def update_venue_img(id):
    form = ImgForm()
    venues = models.Venue.select()
    img_updating = True
    venue = models.Venue.get(models.Venue.id == id)
    if current_user.user_level != "walrus":
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        flash(f"Image for {venue.name} updated","success")
        img = venue_img(form.img.data, venue.name)
        venue_img_update = models.Venue.update(
            img=venue_img(form.img.data, venue.name)
        ).where(models.Venue.id == id)
        venue_img_update.execute()
        return redirect(url_for('admin'))
    return render_template('admin_with_form.html', form=form, venues=venues, venue=venue, img_updating=img_updating)

@app.route('/admin/venue/update/<id>', methods=['GET','POST'])
@login_required
def admin_update_venue(id):
    form = VenueForm()
    venues = models.Venue.select()
    venue = models.Venue.get(models.Venue.id == id)

    form.name.data = venue.name
    form.about.data = venue.about
    form.skid.data = venue.skid

    if current_user.user_level != "walrus":
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        venue_update = models.Venue.update(
            name=form.name.data,
            about=form.about.data,
            skid=form.skid.data
        ).where(models.Venue.id == id)
        venue_update.execute()
        flash(f"Updated information for {venue.name}.")
        return redirect(url_for('admin'))

    return render_template('admin_with_form.html', form=form, venues=venues, venue=venue)

@app.route('/admin/venue/delete/<id>')
@login_required
def delete_venue(id):
    venue = models.Venue.get(models.Venue.id == id)
    if g.user.user_level == "walrus":
        venue_deletion = models.Venue.delete().where(models.Venue.id == venue.id)
        venue_deletion.execute()
        ratings_deletion = models.Rating.delete().where(models.Rating.venue_fk == venue.id)
        ratings_deletion.execute()
        flash(f"Deleted {venue.name}")
        return redirect(url_for('admin'))
    else: 
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))

# ########## BANDS ########## #

@app.route('/admin/add_band', methods=('GET', 'POST'))
@login_required
def add_band():
    form = BandForm()
    bands = models.Band.select()
    if current_user.user_level != "walrus":
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        flash(f"Created band - { form.name.data }", 'success')
        models.Band.create_band(
            name=form.name.data,
            about=form.about.data,
            genre=form.genre.data,
            skid=form.skid.data
        )
        return redirect(url_for('add_band'))
    return render_template('admin_with_form.html', form=form, bands=bands)

@app.route('/admin/band_img/<id>', methods=('GET','POST'))
@login_required
def update_band_img(id):
    form = ImgForm()
    bands = models.Band.select()
    img_updating = True
    band = models.Band.get(models.Band.id == id)
    if current_user.user_level != "walrus":
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        flash(f"Image for {band.name} updated","success")
        img = band_img(form.img.data, band.name)
        band_img_update = models.Band.update(
            img=band_img(form.img.data, band.name)
        ).where(models.Band.id == id)
        band_img_update.execute()
        return redirect(url_for('admin'))
    return render_template('admin_with_form.html', form=form, bands=bands, band=band, img_updating=img_updating)

@app.route('/admin/band/update/<id>', methods=['GET','POST'])
@login_required
def admin_update_band(id):
    form = BandForm()
    bands = models.Band.select()
    band = models.Band.get(models.Band.id == id)
    record = models.Band.select().where(id == models.Band.id).dicts().get()
    if current_user.user_level != "walrus":
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        band_update = models.Band.update(
            name=form.name.data,
            about=form.about.data,
            genre=form.genre.data,
            skid=form.skid.data
        ).where(models.Band.id == id)
        band_update.execute()
        flash(f"Updated information for {band.name}.")
        return redirect(url_for('admin'))

    return render_template('admin_with_form.html', form=form, bands=bands, band=band, record=record)

@app.route('/admin/band/delete/<id>')
@login_required
def delete_band(id):
    band = models.Band.get(models.Band.id == id)
    if g.user.user_level == "walrus":
        band_deletion = models.Band.delete().where(models.Band.id == band.id)
        band_deletion.execute()
        flash(f"Deleted {band.name}")
        return redirect(url_for('admin'))
    else: 
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))




# @app.route('/404') 
# def venue():
#     return render_template('404.html')
