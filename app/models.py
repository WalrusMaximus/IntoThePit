from peewee import *
import datetime, time, moment
import os, psycopg2

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
from playhouse.db_url import connect

if os.environ.get('FLASK_ENV') == "production":
    DATABASE = connect(os.environ.get('DATABASE_URL'))
else:
    DATABASE = PostgresqlDatabase('intothepit')

#--------------# PRIMARY MODELS #--------------#

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True, max_length=256)
    password = CharField(max_length=128)
    avatar = CharField(default="images/user_default.png")
    user_level = CharField(default="user")
    creation_date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password, user_level="user", avatar="images/user_default.png"):
        try:
            cls.create(
                username=username,
                email=email,
                password=generate_password_hash(password),
                avatar=avatar,
                user_level=user_level,
                creation_date=datetime.datetime.now()
            )
        except IntegrityError:
            raise ValueError("User already exists")

class Band(Model):
    name = CharField()
    display_name = CharField()
    about = CharField()
    img = CharField(default="images/band_default.jpg")
    skid = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_band(cls, name, display_name, about, skid, themes="music", img="images/band_default.jpg"):
        try:
            cls.create(
                name=name,
                display_name=display_name,
                about=about,
                img=img,
                skid=skid
            )
        except IntegrityError:
            raise

class Venue(Model):
    name = CharField()
    display_name = CharField()
    img = CharField(default="images/venue_default.jpg")
    about = CharField()
    skid = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_venue(cls, name, display_name, about, skid, img="images/venue_default.jpg"):
        try:
            cls.create(
                name=name,
                display_name=display_name,
                img=img,
                about=about,
                skid=skid
            )
        except IntegrityError:
            raise

class Rating(Model):
    user_fk = ForeignKeyField(
        model=User,
        backref="users"
    )
    venue_fk = ForeignKeyField(
        model=Venue,
        backref="venues",
        null=True
    )
    band_fk = ForeignKeyField(
        model=User,
        backref="bands",
        null=True
    )
    rating = IntegerField()
    rating_type = CharField()
    message = CharField(max_length=1024)

    class Meta:
        database = DATABASE

    @classmethod
    def create_rating(cls,user_fk, rating, rating_type, message, venue_fk=None, band_fk=None):
        try:
            cls.create(
                user_fk=user_fk,
                venue_fk=venue_fk,
                band_fk=band_fk,
                rating=rating,
                rating_type=rating_type,
                message=message,
            )
        except IntegrityError:
            raise

class Favorite(Model):
    user_fk = ForeignKeyField(
        model=User,
        backref="users"
    )
    band_fk = ForeignKeyField(
        model=Band,
        backref="bands",
        null=True
    )
    venue_fk = ForeignKeyField(
        model=Venue,
        backref="venues",
        null=True
    )

    class Meta:
        database = DATABASE

    @classmethod
    def create_favorite(cls,user_fk, band_fk=None, venue_fk=None):
        try:
            cls.create(
                user_fk=user_fk,
                band_fk=band_fk,
                venue_fk=venue_fk,
            )
        except IntegrityError:
            raise


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Band, Venue, Favorite, Rating], safe=True)
    DATABASE.close()







