from flask import render_template, url_for, flash, redirect, g
from app import app, models
from app.forms import LoginForm, RegisterForm, AddUserForm, EditUserForm, VenueForm
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


    # ########## CONTENT PAGES ########## #

@app.route("/", methods=["POST","GET"])
def index():
    form = RegisterForm()
    return render_template('layout.html', title="Into The Pit", form=form)

@app.route("/user") # this will need to be a dynamic route
def user():
    return "User Page Under Construction"

@app.route('/band') # this will need to be a dynamic route
def band():
    return "Band page Under Construction"

@app.route('/venue') # this will need to be a dynamic route
def venue():
    return "Venue page Under Construction"

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
    form = EditUserForm()
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
        flash(f"Deleted {found_venue.name}")
        return redirect(url_for('admin'))
    else: 
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))

# @app.route('/404') 
# def venue():
#     return render_template('404.html')
