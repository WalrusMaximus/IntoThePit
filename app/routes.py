from flask import render_template, url_for, flash, redirect, g, request
from app import app, models
from app.forms import LoginForm, RegisterForm, AddUserForm, EditUserForm, VenueForm, BandForm, RatingForm, AdminEditUserForm, EditRatingForm, AddEventForm
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


    # ########## CONTENT PAGES ########## #

@app.route("/", methods=["POST","GET"])
def index():
    venues = models.Venue.select()
    return render_template('index.html', title="Into The Pit", venues=venues)

@app.route("/user/<id>") # this will need to be a dynamic route
def user(id):
    found_user = models.User.get(models.User.id == id)
    decoder = found_user.avatar.decode()
    location = (f'images/{decoder}')
    avatar = url_for('static', filename=location)
    ratings = models.Rating.select().where(models.Rating.user_fk == found_user.id)
    return render_template('user.html', user=found_user, avatar=avatar, ratings=ratings)

@app.route('/band') # this will need to be a dynamic route
def band():
    return "Band page Under Construction"

@app.route('/venue/<id>/ratings', methods=('GET', 'POST')) # this will need to be a dynamic route
def venue(id):
    found_venue = models.Venue.get(models.Venue.id == id)
    decoder = found_venue.img.decode()
    location = (f'images/{decoder}')
    venue_img = url_for('static', filename=location)
    ratings = models.Rating.select().where(models.Rating.venue_fk == found_venue.id)
    form = RatingForm()
    show_ratings = True
    if form.validate_on_submit():
        locator = models.Rating.select().where(
            (models.Rating.venue_fk == found_venue.id) &
            (models.Rating.user_fk == current_user.id) &
            (models.Rating.rating_type == form.rating_type.data))
        if locator.count() == 0:
            flash(f"Add comment to {found_venue.name}.")
            models.Rating.create_rating(
                user_fk=current_user.id,
                venue_fk=id,
                rating=form.rating.data,
                rating_type=form.rating_type.data,
                message=form.message.data
            )
            return redirect(url_for('venue', id=found_venue.id))
        else:
            flash(f"You can only add one comment per category on each venue")
            return redirect(url_for('venue', id=found_venue.id))
    return render_template('venue.html', venue=found_venue, venue_img=venue_img, ratings=ratings, form=form, id=id, show_ratings=show_ratings)

    # ########## EVENTS ########## #

@app.route('/venue/<id>/events', methods=('GET', 'POST')) # this will need to be a dynamic route
def venue_events(id):
    found_venue = models.Venue.get(models.Venue.id == id)
    decoder = found_venue.img.decode()
    location = (f'images/{decoder}')
    venue_img = url_for('static', filename=location)
    events = models.Event.select().where(models.Event.venue_fk == found_venue.id)
    form = AddEventForm()
    show_events = True
    if form.validate_on_submit():
        if current_user.user_level == "walrus":
            if models.Band.select().where(models.Band.name == form.band.data).exists():
                found_band = models.Band.get(models.Band.name == form.band.data)
                locator = models.Event.select().where(
                    (models.Event.venue_fk == found_venue.id) &
                    (models.Event.band_fk == found_band.id) &
                    (models.Event.date == form.date.data))
                if locator.count() == 0:
                    flash(f"Added event to {found_venue.name} with {form.band.data}.")
                    models.Event.create_event(
                        band_fk=found_band.id,
                        venue_fk=id,
                        date=form.date.data
                    )
                    return redirect(url_for('venue_events', id=found_venue.id))
                flash("Can't add duplicate events","error")
                return redirect(url_for('venue_events', id=found_venue.id))
            flash("Band does not exist in database","error")
            return redirect(url_for('venue_events', id=found_venue.id))
        flash("Not Authorized to Add Events","error")
        return redirect(url_for('venue_events', id=found_venue.id))

    # print(events[0].band_fk.name)
    return render_template('venue.html', venue=found_venue, venue_img=venue_img, events=events, form=form, id=id, show_events=show_events)

    # ########## COMMENTS ########## #

@app.route('/user/delete_rating/<id>', methods=('GET', 'POST'))
def delete_rating(id):
    profile = request.args.get('profile')
    found_rating = models.Rating.get(models.Rating.id == id)
    if found_rating.user_fk.id == current_user.id:
        rating_deletion = models.Rating.delete().where(models.Rating.id == found_rating.id)
        rating_deletion.execute()
        flash(f"Deleted rating on {found_rating.venue_fk.name}")
        if profile == "True":
            return redirect(url_for('user', id=current_user.id))
        return redirect(url_for('venue', id=found_rating.venue_fk.id))
    else:
        flash(f"You cannot delete another users comments","error")
        return redirect(url_for('index'))

@app.route('/user/update_rating/<id>', methods=['GET','POST'])
@login_required
def user_update_rating(id):
    found_user = models.User.get(models.User.id == current_user.id)
    decoder = found_user.avatar.decode()
    location = (f'images/{decoder}')
    avatar = url_for('static', filename=location)


    form = EditRatingForm()
    found_rating = models.Rating.get(models.Rating.id == id)
    ratings = models.Rating.select().where(models.Rating.user_fk == found_user.id)
    if form.validate_on_submit():
        rating_update = models.Rating.update(
            rating=form.rating.data,
            message=form.message.data
        ).where(models.Rating.id == id)
        rating_update.execute()
        flash(f"Updated comment on {found_rating.venue_fk.name}.")
        return redirect(url_for('user',id=current_user.id))

    return render_template('user.html', form=form, found_rating=found_rating, user=found_user, avatar=avatar, ratings=ratings)


@app.route('/venue/update_rating/<id>', methods=('GET', 'POST')) # this will need to be a dynamic route
def venue_update_rating(id):
    found_rating = models.Rating.get(models.Rating.id == id)
    found_venue = models.Venue.get(models.Venue.id == found_rating.venue_fk.id)
    decoder = found_venue.img.decode()
    location = (f'images/{decoder}')
    venue_img = url_for('static', filename=location)
    ratings = models.Rating.select().where(models.Rating.venue_fk == found_venue.id)

    form = EditRatingForm()
    ratings = models.Rating.select().where(models.Rating.venue_fk == found_venue.id)
    if form.validate_on_submit():
        rating_update = models.Rating.update(
            rating=form.rating.data,
            message=form.message.data
        ).where(models.Rating.id == id)
        rating_update.execute()
        flash(f"Updated comment on {found_rating.venue_fk.name}.")
        return redirect(url_for('venue',id=found_venue.id))
    return render_template('venue.html', venue=found_venue, found_rating=found_rating, venue_img=venue_img, ratings=ratings, form=form)

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
            city=form.city.data,
            state=form.state.data,
            zip=form.zip.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
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
            password=form.password.data,
            city=form.city.data,
            state=form.state.data,
            zip=form.zip.data
        )
        return redirect(url_for('add_user'))
    return render_template('admin_with_form.html', form=form, users=users)

@app.route('/admin/user/update/<id>', methods=['GET','POST'])
@login_required
def admin_edit_user(id):
    form = AdminEditUserForm()
    users = models.User.select()
    found_user = models.User.get(models.User.id == id)
    if current_user.user_level != "walrus":
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user_update = models.User.update(
            username=form.username.data,
            user_level=form.user_level.data,
            city=form.city.data,
            state=form.state.data,
            password=generate_password_hash(form.password.data),
            zip=form.zip.data
        ).where(models.User.id == id)
        user_update.execute()
        flash(f"Updated information for {found_user.email}.")
        return redirect(url_for('admin'))

    return render_template('admin_with_form.html', form=form, users=users, found_user=found_user)

@app.route('/user/delete/<id>')
@login_required
def delete_user(id):
    found_user = models.User.get(models.User.id == id)
    if g.user.user_level == "walrus":
        if g.user == found_user:
            flash("We don't condone seppuku here, get someone else to kill your account","error")
            return redirect(url_for('admin'))
        else:
            user_deletion = models.User.delete().where(models.User.id == found_user.id)
            user_deletion.execute()
            ratings_deletion = models.Rating.delete().where(models.Rating.venue_fk == found_user.id)
            ratings_deletion.execute()
            flash(f"Deleted {found_user.username}")
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
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            zip=form.zip.data
        )
        return redirect(url_for('add_venue'))
    return render_template('admin_with_form.html', form=form, venues=venues)

@app.route('/admin/venue/update/<id>', methods=['GET','POST'])
@login_required
def admin_edit_venue(id):
    form = VenueForm()
    venues = models.Venue.select()
    found_venue = models.Venue.get(models.Venue.id == id)
    if current_user.user_level != "walrus":
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        venue_update = models.Venue.update(
            name=form.name.data,
            about=form.about.data,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            zip=form.zip.data
        ).where(models.Venue.id == id)
        venue_update.execute()
        flash(f"Updated information for {found_venue.name}.")
        return redirect(url_for('admin'))

    return render_template('admin_with_form.html', form=form, venues=venues, found_venue=found_venue)

@app.route('/admin/venue/delete/<id>')
@login_required
def delete_venue(id):
    found_venue = models.Venue.get(models.Venue.id == id)
    if g.user.user_level == "walrus":
        venue_deletion = models.Venue.delete().where(models.Venue.id == found_venue.id)
        venue_deletion.execute()
        ratings_deletion = models.Rating.delete().where(models.Rating.venue_fk == found_venue.id)
        ratings_deletion.execute()
        flash(f"Deleted {found_venue.name}")
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
            genre=form.genre.data
        )
        return redirect(url_for('add_band'))
    return render_template('admin_with_form.html', form=form, bands=bands)


@app.route('/admin/band/update/<id>', methods=['GET','POST'])
@login_required
def admin_edit_band(id):
    form = BandForm()
    bands = models.Band.select()
    found_band = models.Band.get(models.Band.id == id)
    if current_user.user_level != "walrus":
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        band_update = models.Band.update(
            name=form.name.data,
            about=form.about.data,
            genre=form.genre.data
        ).where(models.Band.id == id)
        band_update.execute()
        flash(f"Updated information for {found_band.name}.")
        return redirect(url_for('admin'))

    return render_template('admin_with_form.html', form=form, bands=bands, found_band=found_band)

@app.route('/admin/band/delete/<id>')
@login_required
def delete_band(id):
    found_band = models.Band.get(models.Band.id == id)
    if g.user.user_level == "walrus":
        band_deletion = models.Band.delete().where(models.Band.id == found_band.id)
        band_deletion.execute()
        flash(f"Deleted {found_band.name}")
        return redirect(url_for('admin'))
    else: 
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))

# ########## EVENTS ########## #

@app.route('/add_event/<id>', methods=["POST","GET"])
@login_required
def add_event(id):
    form = AddEventForm()
    if current_user.user_level != "walrus":
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        found_band = models.Band.get(models.Band.name == form.band.data)
        flash(f"Created event with { form.name.data }", 'success')
        models.Event.create_band(
            date=form.date.data,
            band_fk=found_band.id,
            venue_fk=id
        )
        return redirect(url_for('add_band'))
    return render_template('admin_with_form.html', form=form, bands=bands)




# @app.route('/404') 
# def venue():
#     return render_template('404.html')
