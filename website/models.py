from . import db
from flask_login import UserMixin
# Using SQLAlchemy ORM for this.
from sqlalchemy.sql import func

# Define data objects that represent database entries.
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(150))
    permission = db.Column(db.String(50), default='user')
    posts = db.relationship('Post')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    desc = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

