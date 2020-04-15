from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from pymongo import MongoClient
from os import environ


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config["SECRET_KEY"] = "VerySecretKey"
client = MongoClient(environ['DB_PORT_27017_TCP_ADDR'], 27017)

app.config.update(dict(
    MAIL_SERVER = 'poczta.o2.pl',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'work.it@o2.pl',
    MAIL_PASSWORD = 'Workit!@#123'
))
   
# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'panel.workit@gmail.com'
# app.config['MAIL_PASSWORD'] = 'Workit!@#123'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
mail = Mail(app) 


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
