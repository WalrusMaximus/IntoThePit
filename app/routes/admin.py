from flask import render_template, url_for, flash, redirect, g, request
from app import app, models, forms
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app.functions import user_img
import os
import cloudinary, cloudinary.uploader, cloudinary.api
from cloudinary.uploader import upload, destroy
from cloudinary.utils import cloudinary_url

# MAIN

@app.route('/admin')
@login_required
def admin():
    if current_user.user_level != "walrus":
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))

    return render_template('admin.html', landing=True)


# USER PAGES

@app.route('/admin/add_user', methods=('GET', 'POST'))
@login_required
def add_user():
    form = forms.AddUserForm()
    users = models.User.select().order_by(models.User.id)
    if current_user.user_level != "walrus":
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        if form.avatar.data:
            img = form.avatar.data
            try:
                uploading = upload(img, overwrite=True, version=1, public_id=form.username.data, folder='user', format="png", width=256, height=255, crops="fill")
                image_query = cloudinary.api.resource(f"user/{form.username.data}")
                avatar = image_query['url']
                models.User.create_user(
                    username=form.username.data,
                    email=form.email.data,
                    user_level=form.user_level.data,
                    password=form.password.data,
                    avatar=avatar
                )
                flash(f"Created user - { form.email.data }", 'success')
                return redirect(url_for('add_user'))
            except:
                flash(f"Couldn't connect to server.. try again later.","error")
                return redirect(url_for('add_user'))
   
        else:
            models.User.create_user(
                username=form.username.data,
                email=form.email.data,
                user_level=form.user_level.data,
                password=form.password.data
            )
            flash(f"Created user - { form.email.data }", 'success')
        
    return render_template('admin.html',
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
        return redirect(url_for('add_user'))

    return render_template('admin.html',
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
            ratings_deletion = models.Rating.delete().where(models.Rating.user_fk == user.id)
            user_deletion = models.User.delete().where(models.User.id == user.id)
            try:
                result = cloudinary.uploader.destroy(f"user/{user.username}")
                ratings_deletion.execute()  
                user_deletion.execute()
                flash(f"Deleted image and account for {user.username}","success")
            except:
                ratings_deletion.execute()  
                user_deletion.execute()
                flash(f"Couldn't reach Cloudinary, image remains for {user.username}","error")
        return redirect(url_for('add_user'))
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
        if form.img.data:
            img = form.img.data
            venue_name = form.name.data.split(" ")
            converted_name = "".join(venue_name)
            try:
                img = form.img.data
                venue_name = form.name.data.split(" ")
                converted_name = "".join(venue_name)
                uploading = upload(img, overwrite=True, public_id=converted_name, folder='venue', format="png", width=512, height=512, crops="lfill")
                image_query = cloudinary.api.resource(f"venue/{converted_name}")
                img = image_query['url']
                models.Venue.create_venue(
                    name=form.name.data,
                    display_name=form.display_name.data,
                    img=img,
                    about=form.about.data,
                    skid=form.skid.data
                )
                flash(f"Created new venue {form.name.data}. CDN Upload Successful","success")
                return redirect(url_for('add_venue'))
            except:
                models.Venue.create_venue(
                    name=form.name.data,
                    display_name=form.display_name.data,
                    about=form.about.data,
                    skid=form.skid.data
                )
                flash(f"Created new venue {form.name.data}, Couldn't Upload to CDN")
                return redirect(url_for('add_venue'))
        else:
            models.Venue.create_venue(
                name=form.name.data,
                display_name=form.display_name.data,
                about=form.about.data,
                skid=form.skid.data
            )
            flash(f"Created new venue - {form.name.data}","success")

        return redirect(url_for('add_venue'))
    return render_template('admin.html', form=form, venues=venues)

@app.route('/admin/venue/update/<id>', methods=['GET','POST'])
@login_required
def admin_update_venue(id):
    form = forms.UpdateVenueForm()
    venues = models.Venue.select()
    venue = models.Venue.get(models.Venue.id == id)
    record = models.Venue.select().where(id == models.Venue.id).dicts().get()

    if current_user.user_level != "walrus":
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        venue_update = models.Venue.update(
            display_name=form.display_name.data,
            about=form.about.data,
            skid=form.skid.data
        ).where(models.Venue.id == id)
        venue_update.execute()
        flash(f"Updated information for {venue.display_name}.")
        return redirect(url_for('add_venue'))

    return render_template('admin.html', form=form, venues=venues, venue=venue, record=record)

@app.route('/admin/venue/delete/<id>')
@login_required
def delete_venue(id):
    venue = models.Venue.get(models.Venue.id == id)
    if g.user.user_level == "walrus":
        favorite_deletion = models.Favorite.delete().where(models.Favorite.venue_fk == venue.id)
        ratings_deletion = models.Rating.delete().where(models.Rating.venue_fk == venue.id)
        venue_deletion = models.Venue.delete().where(models.Venue.id == venue.id)
        try:
            result = cloudinary.uploader.destroy(f"venue/{venue.name}")
            favorite_deletion.execute()
            ratings_deletion.execute()
            venue_deletion.execute()
            flash(f"Deleted account and image for {venue.name}","success")
        except:
            favorite_deletion.execute()
            ratings_deletion.execute()
            venue_deletion.execute()
            flash(f"Couldn't reach Cloudinary, image remains for {venue.name}","error")
        return redirect(url_for('add_venue'))
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
        img = form.img.data
        band_name = form.name.data.split(" ")
        converted_name = "".join(band_name)
        
        if form.img.data:
            try:
                img = form.img.data
                band_name = form.name.data.split(" ")
                converted_name = "".join(band_name)
                uploading = upload(img, overwrite=True, public_id=converted_name, folder='band', format="png", width=512, height=512, crops="lfill")
                image_query = cloudinary.api.resource(f"band/{converted_name}")
                img = image_query['url']
                models.Band.create_band(
                    name=form.name.data,
                    display_name=form.display_name.data,
                    img=img,
                    about=form.about.data,
                    skid=form.skid.data
                )
                flash(f"Created new band {form.name.data}","success")
                return redirect(url_for('add_band'))
            except:
                models.Band.create_band(
                    name=form.name.data,
                    display_name=form.display_name.data,
                    img=img,
                    about=form.about.data,
                    skid=form.skid.data
                )
                flash(f"Created new band {form.name.data}, no CDN access.")
                return redirect(url_for('add_band'))
        else:
            models.Band.create_band(
                name=form.name.data,
                display_name=form.display_name.data,
                about=form.about.data,
                skid=form.skid.data
            )
            flash(f"Created new band {form.name.data}","success")
            return redirect(url_for('add_band'))
        return redirect(url_for('add_band'))
    return render_template('admin.html', form=form, bands=bands)

@app.route('/admin/band/update/<id>', methods=['GET','POST'])
@login_required
def admin_update_band(id):
    form = forms.UpdateBandForm()
    bands = models.Band.select()
    band = models.Band.get(models.Band.id == id)
    record = models.Band.select().where(id == models.Band.id).dicts().get()
    if current_user.user_level != "walrus":
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        if form.img.data:
            img = form.img.data
            band_name = form.name.data.split(" ")
            converted_name = "".join(band_name)
            try:
                uploading = upload(img, overwrite=True, public_id=converted_name, folder='band', format="png", width=512, height=512, crops="lfill")
                image_query = cloudinary.api.resource(f"band/{converted_name}")
                img = image_query['url']
                models.Band.create_band(
                    display_name=form.display_name.data,
                    img=img,
                    about=form.about.data,
                    skid=form.skid.data
                )
                flash(f"Updated {form.name.data}","success")
                return redirect(url_for('admin'))
            except:
                band_update = models.Band.update(
                    display_name=form.display_name.data,
                    about=form.about.data,
                    skid=form.skid.data
                ).where(models.Band.id == id)
                band_update.execute()
                flash(f"Updated {form.display_name.data}, couldn't update CDN","error")
        else:
            band_update = models.Band.update(
                display_name=form.display_name.data,
                about=form.about.data,
                skid=form.skid.data
            ).where(models.Band.id == id)
            band_update.execute()
            flash(f"Updated {form.display_name.data}","success")
            return redirect(url_for('add_band'))

    return render_template('admin.html', form=form, bands=bands, band=band, record=record)

@app.route('/admin/band/delete/<id>')
@login_required
def delete_band(id):
    band = models.Band.get(models.Band.id == id)
    if g.user.user_level == "walrus":
        favorite_deletion = models.Favorite.delete().where(models.Favorite.band_fk == band.id)
        band_deletion = models.Band.delete().where(models.Band.id == band.id)
        try:
            result = cloudinary.uploader.destroy(f"band/{band.name}")
            favorite_deletion.execute()
            band_deletion.execute()
            flash(f"Deleted {band.name} and CDN image","success")
        except:
            favorite_deletion.execute()
            band_deletion.execute()
            flash(f"Deleted {band.name} - Couldn't connect to server to delete image")
        return redirect(url_for('add_band'))
    else: 
        flash("Not authorized to access this page", "error")
        return redirect(url_for('index'))