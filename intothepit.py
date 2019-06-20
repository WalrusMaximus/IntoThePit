import os
from peewee import *
from app import app, models

if __name__ == '__main__':
    if os.environ.get('HEROKU_PRODUCTION'):
        print("Launching in Production Environment")
        PRODUCTION = os.environ.get('PRODUCTION') or True
        app.run(debug=False)
    else:
        models.initialize()
        print("Launching in Development Environment - Debug Active")
        PRODUCTION = os.environ.get('PRODUCTION') or False
        app.run(host='0.0.0.0', debug=True, port=8000)