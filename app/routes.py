from flask import render_template, url_for, flash, redirect, g
from app import app, models
from app.forms import LoginForm, RegisterForm
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


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

@app.route('/admin')
def admin():
    if g.user.user_level != "walrus":
        flash("Not authorized to access this page")
        return redirect(url_for('index'))
    
    users = models.User.select().where(models.User.user_level == "user")

    return render_template('admin.html', users=users)

# @app.route('/404') 
# def venue():
#     return render_template('404.html')
