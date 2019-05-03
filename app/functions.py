# FUNCTIONS
import os
from app import app, models
from PIL import Image

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