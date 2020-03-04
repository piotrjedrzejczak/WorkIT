from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, name, email, password, github, created_on, last_login):
        self._id = self._generate_id()
        self.name = name
        self.email = email
        self.password = password
        self.github = github
        self.created_on = created_on
        self.last_login = last_login

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
