from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from workit.mongo.MongoController import MongoController


app = Flask(__name__)
mongo = MongoController()
login_manager = LoginManager()
login_manager.init_app(app)
app.config["SECRET_KEY"] = "VerySecretKey"
app.config.update(
    dict(
        MAIL_SERVER="poczta.o2.pl",
        MAIL_PORT=465,
        MAIL_USE_TLS=False,
        MAIL_USE_SSL=True,
        MAIL_USERNAME="work.it@o2.pl",
        MAIL_PASSWORD="Workit!@#123",
    )
)
mail = Mail(app)


with app.app_context():
    from . import routes # noqa F401
    from . import auth  # noqa F401
