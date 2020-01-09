from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://dev:workit2020@workitcluster-nege2.mongodb.net/WorkIT?retryWrites=true&w=majority" # noqa E501
app.config["MONGO_DBNAME"] = "WorkIT"
app.config["SECRET_KEY"] = "VerySecretKey"
mongo = PyMongo(app)
collection = mongo.db["Offers"]

from workit import routes  # noqa E402
