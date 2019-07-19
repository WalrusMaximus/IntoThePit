import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Keys(object):
    SONGKICK_API_KEY = os.environ.get('SONGKICK_API_KEY')