from flask import Flask
from pymongo import MongoClient
from os import environ

app = Flask(__name__)
app.config["SECRET_KEY"] = "VerySecretKey"
client = MongoClient(environ['DB_PORT_27017_TCP_ADDR'], 27017)
collection = client.db.offers

from workit import routes  # noqa E402
