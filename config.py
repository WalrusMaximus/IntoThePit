import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = '6278611acd965c39e568f98c7fe05759e8437778db9ac857542d85f450905467'

class Keys(object):
    SONGKICK_API_KEY = 'a5ClIZJ5AtwYU8SR'
    CLOUDINARY_API_SECRET = 'NPI2KPBytqfcT-_9qhGcQ96HRc4'
    CLOUDINARY_API_KEY = '626474955394754'
    CLOUDINARY_CLOUD_NAME = 'intothepit'
    CLOUDINARY_URL = 'CLOUDINARY_URL=cloudinary://626474955394754:NPI2KPBytqfcT-_9qhGcQ96HRc4@intothepit'


# standard API query = https://api.songkick.com/api/3.0/artists/379603/gigography.json?apikey={KEY}
# venue query = https://api.songkick.com/api/3.0/venues/7516/calendar.json?apikey={KEY}


# https://api.songkick.com/api/3.0/artists/527207/calendar.json?apikey={KEY}
# results.event.venue.metroArea to filter by sf bay area
# 
