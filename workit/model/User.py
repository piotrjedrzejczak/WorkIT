from flask_login import UserMixin
from flask import session
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from workit import users_collection


class User(UserMixin):

    def __init__(self, name, email, password, _id=None):
        self._id = uuid4().hex if _id is None else _id
        self.name = name
        self.email = email
        self.password = self.set_password(password)
    
    def get_id(self):
        return self._id

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @classmethod
    def get_by_email(cls, email):
        data = users_collection.find_one({"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_name(cls, name):
        data = users_collection.find_one({"name": name})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, uid):
        data = users_collection.find_one({"_id": uid})
        if data is not None:
            return cls(**data)

    @classmethod
    def register(cls, name, email, password):
        user = cls.get_by_email(email)
        if user is None:
            new_user = cls(name, email, password)
            new_user.save_user()
            session['email'] = email
            return True
        else:
            return False

    def jsonify(self):
        return {
            "_id": self._id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }

    def save_user(self):
        users_collection.insert(self.jsonify())
