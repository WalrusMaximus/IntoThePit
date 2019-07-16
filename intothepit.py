import os
from peewee import *
from app import app, models

if __name__ == '__main__':
    if os.environ.get('FLASK_ENV') == "production":
        print("Launching in Production Environment")
        models.initialize()
        app.run(debug=False)
    else:
        models.initialize()
        print("Launching in Development Environment - Debug Active")
        app.run(host='0.0.0.0', debug=True, port=8000)