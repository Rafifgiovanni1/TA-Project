from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from .. import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    role = db.Column(db.String(60), nullable=False)

    def __init__(self, username, email, password, role):
        self.username: str = username
        self.email: str = email
        self.password: str = generate_password_hash(password, method="SHA256")
        self.role: str = role

    def add(self):
        db.session.add(self)
        db.session.commit()
