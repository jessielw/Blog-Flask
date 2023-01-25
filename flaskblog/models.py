from datetime import datetime

import itsdangerous.exc
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedSerializer
from sqlalchemy.exc import OperationalError

from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except OperationalError:
        return None


class User(db.Model, UserMixin):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="images/default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def get_reset_token(self):
        s = TimedSerializer(current_app.secret_key)
        return s.dumps({"id": self.id})

    @staticmethod
    def verify_reset_token(token, expires_seconds: int = 1800):
        s = TimedSerializer(current_app.secret_key)
        try:
            user_id = s.loads(token, expires_seconds)
        except itsdangerous.exc.SignatureExpired:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


def create_table_if_not_exist(app):
    with app.app_context():
        db.create_all()
        # db.session.commit()
