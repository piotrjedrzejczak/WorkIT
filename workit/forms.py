from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, RadioField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from workit.const import CATEGORIES


class SearchForm(FlaskForm):
    keyword = StringField('Keyword')
    submitLogin = SubmitField('Log In')
    cities = RadioField('City', choices=[
        ('', 'All'),
        ('Warszawa', 'Warszawa'),
        ('Krakow', 'Kraków'),
        ('Wroclaw', 'Wrocław'),
        ('Poznan', 'Poznań'),
        ('Lodz', 'Łódź'),
        ('Gdansk', 'Gdańsk')
    ], default='')
    categories = RadioField('Category', choices=[('', 'All')] + [
            (label, value)
            for label, value in zip(
                CATEGORIES.keys(), CATEGORIES.keys()
            )
        ], default='')
    submit = SubmitField('Search')


class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[
        Length(min=6),
        Email(message='Enter a valid email.'),
        DataRequired()]
    )
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must have at least six characters.')]
    )
    confirm = PasswordField('Confirm Your password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )
    github = StringField('Github', validators=[Optional()])
    submitSignup = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Enter a valid email.')]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    submitLogin = SubmitField('Log In')
