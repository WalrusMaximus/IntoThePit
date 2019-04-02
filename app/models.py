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
    avatar = BlobField(default="default.png")
    city = CharField()
    state = CharField()
    zip = CharField()
    user_level = CharField(default="user")

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password, city, state, zip, user_level="user", avatar="default.png"):
        try:
            cls.create(
                username=username,
                email=email,
                password=generate_password_hash(password),
                avatar="default.png",
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
    genre = CharField()
    themes = CharField()
    img = BlobField(default="default_band.png")
    bigimg = BlobField(default="default_band_bg.png")

    class Meta:
        database = DATABASE

    @classmethod
    def create_band(cls, name, about, genre, themes, img="default_band.png", bigimg="default_band_bg.png"):
        try:
            cls.create(
                name=name,
                about=about,
                genre=genre,
                themes=themes,
                img="default_band.png",
                bigimg="default_band_bg.png"
            )
        except IntegrityError:
            raise

class Venue(Model):
    name = CharField()
    img = BlobField(default="default_venue.png")
    about = CharField()
    address = CharField()
    city = CharField()
    state = CharField()
    zip = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_venue(cls, name, about, address, city, state, zip, img="default_venue.png"):
        try:
            cls.create(
                name=name,
                img="default_venue.png",
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
    message = CharField(max_length=1024)

    class Meta:
        database = DATABASE

    @classmethod
    def create_rating(cls,user_fk, venue_fk, band_fk, rating, message):
        try:
            cls.create(
                user_fk=user_fk,
                venue_fk=venue_fk,
                band_fk=band_fk,
                rating=rating,
                message=message,
            )
        except IntegrityError:
            raise

class Event(Model):
    band_fk = ForeignKeyField(
        model=User,
        backref="bands",
        null=True
    )
    venue_fk = ForeignKeyField(
        model=Venue,
        backref="venues",
        null=True
    )
    date = DateTimeField()

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

class FavBand(Model):
    user_fk = ForeignKeyField(
        model=User,
        backref="users"
    )
    band_fk = ForeignKeyField(
        model=User,
        backref="bands",
        null=True
    )

    class Meta:
        database = DATABASE

    @classmethod
    def create_favband(cls,user_fk,band_fk):
        try:
            cls.create(
                user_fk=user_fk,
                band_fk=band_fk
            )
        except IntegrityError:
            raise


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Band, Venue, Event, Friend, FavBand, Rating], safe=True)
    DATABASE.close()







