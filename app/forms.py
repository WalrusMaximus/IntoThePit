import datetime, time

from flask_wtf import FlaskForm
from app.models import User, Band, Venue, Favorite, Rating
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, ValidationError, Length, Email, EqualTo, Regexp

def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that name already exists.')


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')

def venue_exists(form, field):
    if Venue.select().where(Venue.name == field.data).exists():
        raise ValidationError('A venue with that name already exists.')

def band_exists(form, field):
    if Band.select().where(Band.name == field.data).exists():
        raise ValidationError('A band with that name already exists.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
            DataRequired(),
            Length(max=256),
            Email()
        ])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
            DataRequired(),  
            Regexp(r'^[a-zA-Z0-9 ]+$',
                message=("Name cannot contain symbols or special characters")
            ),
            Length(min=2, max=32),
            name_exists
        ])
    email = StringField('Email', validators=[DataRequired(), Length(max=256), Email(), email_exists])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[
            DataRequired(),  
            Regexp(r'^[a-zA-Z0-9 ]+$',
                message=("Name cannot contain symbols or special characters")
            ),
            Length(min=2, max=32),
            name_exists
        ])
    email = StringField('Email', validators=[DataRequired(), Length(max=256), Email(), email_exists])
    user_level = SelectField(
        'User Level',
        choices=[("user", 'user'), ("walrus", 'walrus')],
        default="user"
    )
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create')

class AdminUpdateUserForm(FlaskForm):
    user_level = SelectField(
        'User Level',
        choices=[("user", 'user'), ("walrus", 'walrus')],
        default="user"
    )
    submit = SubmitField('Commit Changes')

class UpdateUserForm(FlaskForm):
    avatar = FileField('Update Profile Picture', validators=[DataRequired(),FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Commit Changes')

class VenueForm(FlaskForm):
    name = StringField('Name', validators=[
            DataRequired(),  
            Regexp(r'^[a-zA-Z0-9 ]+$',
                message=("Name cannot contain symbols or special characters")
            ),
            Length(min=2, max=128),
        ])
    about = StringField("About", validators=[DataRequired()])
    skid = StringField("Songkick ID", validators=[DataRequired()])
    submit = SubmitField('Create')

class BandForm(FlaskForm):
    name = StringField('Name', validators=[
            DataRequired(),  
            Regexp(r'^[a-zA-Z0-9 ]+$',
                message=("Name cannot contain symbols or special characters")
            ),
        ])
    about = StringField("About", validators=[DataRequired()])
    genre = StringField("Genre", validators=[DataRequired()])
    skid = StringField("Songkick ID", validators=[DataRequired()])
    submit = SubmitField('Create')

class RatingForm(FlaskForm):
    rating = SelectField(
        'Rating = 1-5',
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        default="5"
    )
    rating_type = SelectField(
        'What are you Rating?',
        choices=[("Overall", 'Overall'), ("Mosh Pit", 'Mosh Pit'), ("Sound", 'Sound'), ("Facilities", 'Facilities')]
    )
    message = StringField('Tell us what you think...', validators=[DataRequired(), Length(max=512)])
    submit = SubmitField("Submit")

class UpdateRatingForm(FlaskForm):
    rating = SelectField(
        'Rating = 1-5',
        choices=[("1", '1'), ("2", '2'), ("3", '3'), ("4", '4'), ("5", '5')],
        default="5"
    )
    message = StringField('Tell us what you think...', validators=[DataRequired(), Length(max=512)])
    submit = SubmitField("Submit")

class ImgForm(FlaskForm):
    img = FileField('Update Profile Picture', validators=[DataRequired(),FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Commit Changes')
    
