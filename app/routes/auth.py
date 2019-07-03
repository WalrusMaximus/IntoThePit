from flask import render_template, url_for, flash, redirect
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import current_user, login_required, login_user, logout_user 
from app import app, models, forms
from app.config import Keys
import os

@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()

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

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        admin_access = False
        print("Env", os.environ.get('ADMIN'))
        print(Keys.ADMIN)
        if os.environ.get('ADMIN'):
            if form.email.data == os.environ.get('ADMIN'):
                admin_access = True
        if Keys.ADMIN == form.email.data:
            admin_access = True
        if admin_access:
            models.User.create_user(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                user_level="walrus"
            )
            user = models.User.get(models.User.email == form.email.data)
            flash(f"Registered Admin { form.email.data }", 'success')
            login_user(user)
        else:
            models.User.create_user(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                user_level="user"
            )
            user = models.User.get(models.User.email == form.email.data)
            flash(f"Registered { form.email.data }", 'success')
            login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out", "success")
    return redirect(url_for('index'))
