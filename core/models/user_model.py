import datetime
from flask_mongoengine import Document
from flask_mongoengine.wtf import model_form
from core import db
from passlib.hash import pbkdf2_sha256 as sha256


class User(db.Document):
    name = db.StringField(required=True, max_length=20, unique=True,)
    password = db.StringField(required=True)
    actions_performed = db.IntField()
    cooldown_started = db.DateTimeField()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


