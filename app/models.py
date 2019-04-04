from peewee import *
import datetime, time, moment

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('intothepit.db')

#--------------# PRIMARY MODELS #--------------#

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True, max_length=256)
    password = CharField(max_length=128)
    avatar = BlobField(default="images/default.png")
    city = CharField()
    state = CharField()
    zip = CharField()
    user_level = CharField(default="user")

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password, city, state, zip, user_level="user", avatar="images/default.png"):
        try:
            cls.create(
                username=username,
                email=email,
                password=generate_password_hash(password),
                avatar="images/default.png",
                user_level=user_level,
                city=city,
                state=state,
                zip=zip
            )
        except IntegrityError:
            raise ValueError("User already exists")

class Band(Model):
    name = CharField()
    about = CharField()
    genre = CharField(null=True)
    themes = CharField(null=True, default="music")
    img = BlobField(default="images/default_band.jpg")
    bigimg = BlobField(default="images/default_band_bg.jpg")

    class Meta:
        database = DATABASE

    @classmethod
    def create_band(cls, name, about, genre, themes="music", img="images/default_band.jpg", bigimg="images/default_band_bg.jpg"):
        try:
            cls.create(
                name=name,
                about=about,
                genre=genre,
                img="images/default_band.jpg",
                bigimg="images/default_band_bg.jpg"
            )
        except IntegrityError:
            raise

class Venue(Model):
    name = CharField()
    img = BlobField(default="images/default_venue.jpg")
    about = CharField()
    address = CharField()
    city = CharField()
    state = CharField()
    zip = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_venue(cls, name, about, address, city, state, zip, img="images/default_venue.jpg"):
        try:
            cls.create(
                name=name,
                img="images/default_venue.jpg",
                about=about,
                address=address,
                city=city,
                state=state,
                zip=zip
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

class Event(Model):
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
    date = DateField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_event(cls,band_fk,venue_fk,date):
        try:
            cls.create(
                band_fk=band_fk,
                venue_fk=venue_fk,
                date=date
            )
        except IntegrityError:
            raise

class Friend(Model):
    friender = ForeignKeyField(
        model=User,
        backref="friends"
    )
    friendee = ForeignKeyField(
        model=User,
        backref="friends",
        null=True
    )

    class Meta:
        database = DATABASE

    @classmethod
    def create_friend(cls,friender,friendee):
        try:
            cls.create(
                friender=friender,
                friendee=friendee
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
    def create_favorite(cls,user_fk, band_fk, venue_fk):
        try:
            cls.create(
                user_fk=user_fk,
                band_fk=band_fk,
                venue_fk=venue_fk
            )
        except IntegrityError:
            raise


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Band, Venue, Event, Friend, Favorite, Rating], safe=True)
    DATABASE.close()







