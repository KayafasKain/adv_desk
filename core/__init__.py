from json import dumps
import json
from flask import Flask, send_from_directory
from flask_login import login_required, LoginManager, current_user
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
import os



app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = '245rwefsdvbcbert3rgdfgh34'
jwt = JWTManager(app)

app.config['MONGODB_SETTINGS'] = {
    'db': 'adv_board',
    'host': 'mongodb://lab_master:lab_master1@ds147180.mlab.com:47180/adv_board'
}


db = MongoEngine()
db.init_app(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = '/auth/login'

from core.controllers import user_controller
app.register_blueprint(blueprint=user_controller.user_ctrl, url_prefix='/user')

from core.controllers import post_controller
app.register_blueprint(blueprint=post_controller.post_ctrl, url_prefix='/post')

from core.controllers import comment_controller
app.register_blueprint(blueprint=comment_controller.comment_ctrl, url_prefix='/comment')




