from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, RadioField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, url
from workit.const import FORM_CITY_CHOICES, FORM_CATEGORY_CHOICES


class SearchForm(FlaskForm):
    keyword = StringField("Keyword")
    cities = RadioField(
        "City",
        choices=FORM_CITY_CHOICES,
        default=""
    )
    categories = RadioField(
        "Category",
        choices=FORM_CATEGORY_CHOICES,
        default=""
    )
    submit = SubmitField("Search")


class SignupForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField(
        "Email",
        validators=[
            Length(min=6),
            Email(message="Enter a valid email."),
            DataRequired(),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, message="Password must have at least six characters."),
        ],
    )
    confirm = PasswordField(
        "Confirm Your password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    github = StringField("Github", validators=[Optional()])
    submitSignup = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField(
        "Email", validators=[DataRequired(), Email(message="Enter a valid email.")]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submitLogin = SubmitField("Log In")


class EditProfileForm(FlaskForm):
    nameEdit = StringField("Name", validators=[DataRequired()])
    githubEdit = StringField(
        "Github", validators=[url(message="Enter a valid Github URL"), Optional()]
    )
    emailEdit = StringField(
        "Email", validators=[DataRequired(), Email(message="Enter a valid email.")]
    )
    submitEdit = SubmitField("Submit")
