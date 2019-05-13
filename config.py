import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '6278611acd965c39e568f98c7fe05759e8437778db9ac857542d85f450905467'
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

class Keys(object):
    SONGKICK_API_KEY = os.environ.get('SONGKICK_API_KEY') or 'a5ClIZJ5AtwYU8SR'



# standard API query = https://api.songkick.com/api/3.0/artists/379603/gigography.json?apikey={KEY}
# venue query = https://api.songkick.com/api/3.0/venues/7516/calendar.json?apikey={KEY}


# https://api.songkick.com/api/3.0/artists/527207/calendar.json?apikey={KEY}
# results.event.venue.metroArea to filter by sf bay area
# 