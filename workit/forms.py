from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, RadioField
from workit.const import CATEGORIES


class SearchForm(FlaskForm):
    keyword = StringField('Keyword')
    cities = RadioField('City', choices=[
        ('', 'All'),
        ('Warszawa', 'Warszawa'),
        ('Krakow', 'Kraków'),
        ('Wroclaw', 'Wrocław'),
        ('Poznan', 'Poznań'),
        ('Lodz', 'Łódź'),
        ('Gdansk', 'Gdańsk')
    ])
    categories = RadioField('Category', choices=[('', 'All')] + [
            (label, value)
            for label, value in zip(
                CATEGORIES.keys(), CATEGORIES.keys()
            )
        ])
    submit = SubmitField('Search')
