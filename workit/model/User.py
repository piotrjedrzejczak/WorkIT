from flask_login import UserMixin
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from workit import mongo


class User(UserMixin):

    def __init__(self, name, email, password, github, _id=None):
        self._id = uuid4().hex if _id is None else _id
        self.name = name
        self.email = email
        self.password = password
        self.github = github

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_id(self):
        return self._id

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get_by_id(cls, _id):
        data = mongo.users.find_one({"_id": _id})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_name(cls, name):
        data = mongo.users.find_one({"name": name})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_email(cls, email):
        data = mongo.users.find_one({"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_github(cls, github):
        data = mongo.users.find_one({"github": github})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_password(cls, password):
        data = mongo.users.find_one({"password": password})
        if data is not None:
            return cls(**data)

    def jsonify(self):
        return self.__dict__

    def save_user(self):
        mongo.users.insert(self.jsonify())
