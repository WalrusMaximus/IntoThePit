from flask import render_template, url_for, flash, redirect
from app import app, models, forms
from flask_login import current_user, login_required

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
