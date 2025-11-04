from app import db
from flask_login import UserMixin

class Role:
    ADMIN = 'admin'
    TRAINER = 'trainer'
    MEMBER = 'member'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default=Role.MEMBER)

    def is_admin(self):
        return self.role == Role.ADMIN

    def is_trainer(self):
        return self.role == Role.TRAINER
