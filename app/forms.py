from flask_wtf import FlaskForm
from app.models import User, Band, Venue, FavBand, Rating, Friend, Event
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
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
    city = StringField("City", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired()])
    zip = StringField("Zip", validators=[DataRequired()])
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
    city = StringField("City", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired()])
    zip = StringField("Zip", validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create')

class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[
            DataRequired(),  
            Regexp(r'^[a-zA-Z0-9 ]+$',
                message=("Name cannot contain symbols or special characters")
            ),
            Length(min=2, max=32),
            name_exists
        ])
    user_level = SelectField(
        'User Level',
        choices=[("user", 'user'), ("walrus", 'walrus')],
        default="user"
    )
    city = StringField("City", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired()])
    zip = StringField("Zip", validators=[DataRequired()])
    submit = SubmitField('Commit Changes')

class AddVenueForm(FlaskForm):
    name = StringField('Name', validators=[
            DataRequired(),  
            Regexp(r'^[a-zA-Z0-9 ]+$',
                message=("Name cannot contain symbols or special characters")
            ),
            Length(min=2, max=128),
            venue_exists
        ])
    about = StringField("About", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired()])
    zip = StringField("Zip", validators=[DataRequired()])
    submit = SubmitField('Create')
    

