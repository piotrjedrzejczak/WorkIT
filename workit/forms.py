from workit.const import FORM_CITY_CHOICES, FORM_CATEGORY_CHOICES
from re import match, IGNORECASE
from flask_wtf import FlaskForm
from wtforms.widgets import html_params, CheckboxInput, HTMLString
from wtforms import (
    SubmitField,
    StringField,
    IntegerField,
    RadioField,
    PasswordField,
    SelectMultipleField,
    ValidationError
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional,
    NumberRange
)


# WIDGETS #


class MultipleCheckboxWidget:

    def __init__(self, html_tag='div', prefix_label=False):
        self.html_tag = html_tag
        self.prefix_label = prefix_label

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = [f'<{self.html_tag} {html_params(**kwargs)}>']
        for subfield in field:
            if self.prefix_label:
                html.append(f'<div>{subfield.label} {subfield()}</div>')
            else:
                html.append(f'<div>{subfield()} {subfield.label}</div>')
        return HTMLString(''.join(html))


# VALIDATORS #


def validate_github_url(form, field):
    message = 'Invalid GitHub Address, expected https://github.com/<your_username_here>'
    valid = match(
        r'(https:\/\/)github.com\/.*|github.com\/.*',
        field.data,
        flags=IGNORECASE
    )
    if not valid:
        raise ValidationError(message)


# FIELDS #


class MultipleCheckboxField(SelectMultipleField):

    widget = MultipleCheckboxWidget()
    option_widget = CheckboxInput()


# FORMS #


class SearchForm(FlaskForm):
    keyword = StringField("Keyword")
    cities = RadioField("City", choices=FORM_CITY_CHOICES, default="")
    categories = RadioField("Category", choices=FORM_CATEGORY_CHOICES, default="")
    submit = SubmitField("Search")


class SignupForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField(
        "Email",
        validators=[Email(message="Enter valid email address"), DataRequired()],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6, message="Password has to be at least 6 charachters long."),
        ],
    )
    confirm = PasswordField(
        "Confirm Your password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords are not matching."),
        ],
    )
    github = StringField("Github", validators=[Optional(), validate_github_url])
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Enter valid email address.")],
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class ChangePasswordForm(FlaskForm):

    old_password = PasswordField("Old Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired()])
    confirm_new = PasswordField(
        "Confirm Your New Password",
        validators=[
            DataRequired(),
            EqualTo("new_password", message="Passwords are not matching."),
        ],
    )
    submit = SubmitField("Change")


class ChangeNameForm(FlaskForm):
    new_name = StringField('New Name', validators=[DataRequired()])
    submit = SubmitField('Change')


class ChangeEmailForm(FlaskForm):
    new_email = StringField(
        'New Email Address', validators=[
            Email(message="Enter valid email address."),
            DataRequired()
        ]
    )
    confirm_email = StringField(
        'New Email Address', validators=[
            Email(message="Enter valid email address."),
            EqualTo('new_email', message='Emails are not matching.'),
            DataRequired()
        ]
    )
    submit = SubmitField('Change')


class ChangeGithubURLForm(FlaskForm):
    new_github_url = StringField(
        'New Github Profile URL', validators=[
            DataRequired(),
            validate_github_url
        ]
    )
    submit = SubmitField('Change')


class NewsletterForm(FlaskForm):
    locations = MultipleCheckboxField(choices=FORM_CITY_CHOICES)
    categories = MultipleCheckboxField(choices=FORM_CATEGORY_CHOICES)
    keywords = StringField("Keywords")
    max_results = IntegerField(
        "How many results do you want to recive?",
        validators=[
            NumberRange(min=1, max=30, message='Wrong number, pick between 1 and 30.')
        ]
    )
    frequency = IntegerField(
        "How often would you like to receive the newsletter?",
        validators=[
            NumberRange(min=1, max=14, message='Wrong number, pick between 1 and 14.')
        ]
    )
    submit = SubmitField('Confirm')
