from flask import Flask
from flask_login import LoginManager
from pymongo import MongoClient
from os import environ


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config["SECRET_KEY"] = "VerySecretKey"
client = MongoClient(environ['DB_PORT_27017_TCP_ADDR'], 27017)

users_collection = client.db.users
newsletters_collection = client.db.newsletters
offers_collection = client.db.offers
offers_collection.create_index(
    [('title', 'text'), ('techstack', 'text')],
    default_language='english'
)

with app.app_context():
    from . import routes
    from . import auth # noqa F401

from workit import routes  # noqa E402
