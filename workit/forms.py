from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    keyword = StringField('Keyword', validators=[DataRequired()])
    submit = SubmitField('Search')
