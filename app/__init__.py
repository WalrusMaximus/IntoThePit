from flask import Flask, url_for
# from flask_assets import Environment, Bundle
# from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.static_folder = 'static'
# assets = Environment(app)
app.config['SECRET_KEY'] = "beepboopiamrobotbeepboop"
# scss = Bundle('main.scss', filters='pyscss', output='styles.css')
# assets.register('scss_all',scss)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/server'
# db = SQLAlchemy(app)

from app import routes
