import datetime
from flask_mongoengine import Document
from flask_mongoengine.wtf import model_form
from core import db


class Post(db.Document):
    slug = db.StringField(required=True, max_length=20, unique=True)
    creator = db.StringField(required=True, max_length=20)
    title = db.StringField(required=True, max_length=50)
    created_at = db.DateTimeField()
    comments = db.ListField()
    rates = db.ListField()



