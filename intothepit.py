import os
from peewee import *
from app import app, models

if 'ON_HEROKU' in os.environ:
    models.initialize()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    models.initialize()
    app.run(host='0.0.0.0', debug=True, port=port)