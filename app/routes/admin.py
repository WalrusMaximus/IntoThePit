from flask import render_template, url_for, flash, redirect, g, request
from app import app, models, forms
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app.functions import user_img, band_img, venue_img
from app.config import Keys
import os
import cloudinary, cloudinary.uploader, cloudinary.api
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

# MAIN

@app.route('/admin')
@login_required
def admin():
    if current_user.user_level != "walrus":
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))
    
    users = models.User.select()
    venues = models.Venue.select().order_by(models.Venue.name)
    bands = models.Band.select().order_by(models.Band.name)

    return render_template('admin.html',
        users=users,
        venues=venues,
        bands=bands
    )


# USER PAGES

@app.route('/admin/add_user', methods=('GET', 'POST'))
@login_required
def add_user():
    form = forms.AddUserForm()
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
    return render_template('admin_with_form.html',
        form=form,
        users=users
    )

@app.route('/admin/user/update/<id>', methods=['GET','POST'])
@login_required
def admin_update_user(id):
    form = forms.AdminUpdateUserForm()
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

    return render_template('admin_with_form.html',
        form=form,
        users=users,
        user=user
    )

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
            ratings_deletion = models.Rating.delete().where(models.Rating.user_fk == user.id)
            ratings_deletion.execute()
            flash(f"Deleted {user.username}")
            return redirect(url_for('admin'))
    else: 
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))
        
# VENUES

@app.route('/admin/add_venue', methods=('GET', 'POST'))
@login_required
def add_venue():
    form = forms.VenueForm()
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
    form = forms.ImgForm()
    venues = models.Venue.select()
    img_updating = True
    venue = models.Venue.get(models.Venue.id == id)
    if current_user.user_level != "walrus":
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        img = form.img.data
        venue_name = venue.name.split(" ")
        converted_name = "".join(venue_name)
        try:
            uploading = upload(img, overwrite=True, public_id=converted_name, folder='venue', format="png", width=256, height=255, crops="fill")
            image_query = cloudinary.api.resource(f"venue/{venue.name}")
            img = image_query['url']
            venue_update = models.Venue.update(
                img=img
            ).where(models.Venue.id == id)
            venue_update.execute()
            flash(f"Image for {venue.name} updated","success")
            print(img)
            return redirect(url_for('admin'))
        except:
            flash(f"Couldn't connect to server... try again.","error")
            return redirect(url_for('update_venue_img',id=id))
    return render_template(
        'admin_with_form.html',
        form=form,
        venues=venues,
        venue=venue,
        img_updating=img_updating
    )

@app.route('/admin/venue/update/<id>', methods=['GET','POST'])
@login_required
def admin_update_venue(id):
    form = forms.VenueForm()
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
        favorite_deletion = models.Favorite.delete().where(models.Favorite.venue_fk == venue.id)
        favorite_deletion.execute()
        ratings_deletion = models.Rating.delete().where(models.Rating.venue_fk == venue.id)
        ratings_deletion.execute()
        venue_deletion = models.Venue.delete().where(models.Venue.id == venue.id)
        venue_deletion.execute()
        flash(f"Deleted {venue.name}")
        return redirect(url_for('admin'))
    else: 
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))

# BANDS

@app.route('/admin/add_band', methods=('GET', 'POST'))
@login_required
def add_band():
    form = forms.BandForm()
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
    form = forms.ImgForm()
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
    form = forms.BandForm()
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
        favorite_deletion = models.Favorite.delete().where(models.Favorite.band_fk == band.id)
        favorite_deletion.execute()
        band_deletion = models.Band.delete().where(models.Band.id == band.id)
        band_deletion.execute()
        flash(f"Deleted {band.name}")
        return redirect(url_for('admin'))
    else: 
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))