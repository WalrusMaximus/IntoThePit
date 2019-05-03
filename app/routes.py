from flask import render_template, url_for, flash, redirect, g, request
from app import app, models, forms
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# ########## FUNCTIONS ########## #

from app.functions import user_img, venue_img, band_img

# ########## ROUTES ########## #

from app.route_paths import admin, auth, band, main, user, venue



