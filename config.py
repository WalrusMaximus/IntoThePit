import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '6278611acd965c39e568f98c7fe05759e8437778db9ac857542d85f450905467'
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

class Keys(object):
    SONGKICK_API_KEY = os.environ.get('SONGKICK_API_KEY') or 'a5ClIZJ5AtwYU8SR'
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET') or 'NPI2KPBytqfcT-_9qhGcQ96HRc4'
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY') or '626474955394754'
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME') or 'intothepit'

# standard API query = https://api.songkick.com/api/3.0/artists/379603/gigography.json?apikey={KEY}
# venue query = https://api.songkick.com/api/3.0/venues/7516/calendar.json?apikey={KEY}


# https://api.songkick.com/api/3.0/artists/527207/calendar.json?apikey={KEY}
# results.event.venue.metroArea to filter by sf bay area
# 

# AWSAKI c66089a527315dedf6411a8d80e55852daaf8078c64bd6605cda607f2dde2757
# AWSAK a18423d73f1d46018c50233af27297e481075171fd9c054fd89cd988003bd5c2