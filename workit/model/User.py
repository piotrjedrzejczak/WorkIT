from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from workit import mongo
from uuid import uuid4


class User(UserMixin):

    password_hash = None

    def __init__(self, name, email, github, _id=None):
        self._id = uuid4().hex if _id is None else _id
        self.name = name
        self.email = email
        self.github = github

    def __repr__(self):
        return f'User {self.name}'

    def get_id(self):
        return self._id

    @property
    def password(self):
        raise AttributeError('Write Only.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, method='sha256')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_field(self, field, value):
        transaction = mongo.users.update_one(
            {'_id': self._id},
            {'$set': {field: value}}
        )
        return transaction.acknowledged

    def save_user(self):
        if self.password_hash:
            mongo.users.insert(self.__dict__)
        else:
            raise AttributeError('Password Not Set.')

    @staticmethod
    def get_by_id(id):
        found_user = mongo.users.find_one({'_id': id})
        if found_user:
            user = User(
                found_user["name"],
                found_user["email"],
                found_user["github"],
                found_user["_id"]
            )
            user.password_hash = found_user["password_hash"]
            return user
        return None

    @staticmethod
    def get_by_email(email):
        found_user = mongo.users.find_one({'email': email})
        if found_user:
            user = User(
                found_user["name"],
                found_user["email"],
                found_user["github"],
                found_user["_id"]
            )
            user.password_hash = found_user["password_hash"]
            return user
        return None
