import datetime
from flask_mongoengine import Document
from flask_mongoengine.wtf import model_form
from core import db


class Comment(db.Document):
    creator = db.StringField(required=True, max_length=20)
    text = db.StringField(required=True, max_length=255)




