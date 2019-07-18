# FUNCTIONS
import os
import cloudinary, cloudinary.uploader, cloudinary.api
from cloudinary.uploader import upload, destroy
from cloudinary.utils import cloudinary_url


def user_img(img):
    uploading = upload(img, overwrite=True, version=1, public_id=user.username, folder='user', format="png", width=256, height=255, crops="fill")
    image_query = cloudinary.api.resource(f"user/{user.username}")
    avatar = image_query['url']
    return avatar
