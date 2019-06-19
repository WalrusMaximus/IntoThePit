import os
from peewee import *
from app import app, models

if __name__ == '__main__':
    if os.environ['ENV'] == 'prod':
        app.run(debug=False)
    else:
        models.initialize()
        app.run(host='0.0.0.0', debug=True, port=port)