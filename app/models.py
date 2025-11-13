from app import db, login
from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash

class Role:
    ADMIN = 'admin'
    TRAINER = 'trainer'
    MEMBER = 'member'

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    role = db.Column(db.String(20), default=Role.MEMBER)

    def is_admin(self):
        return self.role == Role.ADMIN

    def is_trainer(self):
        return self.role == Role.TRAINER
    
    def is_member(self):
        return self.role == Role.MEMBER

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    trainer_name = db.Column(db.String(128))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))




















