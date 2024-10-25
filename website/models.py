from . import db
from flask_login import UserMixin
from datetime import datetime
from datetime import timedelta

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    deadline = db.Column(db.DateTime(timezone = True), default = lambda: datetime.now() + timedelta(day = 1))
    content = db.Column(db.String(300), nullable = False)
    userID = db.Column(db.Integer, db.ForeignKey("user.id"))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(150), nullable = False, unique = True)
    password = db.Column(db.String(170), nullable = False)
    tasks = db.relationship("Task")




