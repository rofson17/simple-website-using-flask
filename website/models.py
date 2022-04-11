from datetime import datetime

from . import DB


class Users(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(150), nullable=False)
    email = DB.Column(DB.String(70), unique=True, nullable=False)
    photo = DB.Column(DB.String(200), default='default_image.png')
    password = DB.Column(DB.String(150), nullable=False)
    date = DB.Column(DB.DateTime, default=datetime.utcnow())


class Contacts(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(150), nullable=False)
    email = DB.Column(DB.String(150),  nullable=False)
    subject = DB.Column(DB.String(150), nullable=False)
    message = DB.Column(DB.String(250), nullable=False)
    date = DB.Column(DB.DateTime, default=datetime.utcnow())
