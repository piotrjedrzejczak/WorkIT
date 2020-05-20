from flask import Flask
from flask_mail import Mail
from flask_login import LoginManager
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from workit.mongo.MongoController import MongoController


app = Flask(__name__)
app.config["SECRET_KEY"] = "VerySecretKey"
app.config["MAIL_SERVER"] = "poczta.o2.pl"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "work.it@o2.pl"
app.config["MAIL_PASSWORD"] = "Workit!@#123"
scheduler = BackgroundScheduler(timezone='utc', deamon=True)
login_manager = LoginManager()
login_manager.init_app(app)
mongo = MongoController()
mail = Mail(app)

with app.app_context():
    from . import routes # noqa F401
    from . import auth  # noqa F401
    from .tasks import send_newsletters, refresh_offers
    delay = timedelta(minutes=5)
    scheduler.add_job(refresh_offers, 'interval', hours=24, next_run_time=datetime.now())
    scheduler.add_job(send_newsletters, 'interval', hours=24, next_run_time=datetime.now() + delay)
    scheduler.start()
