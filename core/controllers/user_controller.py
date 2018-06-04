from flask import Blueprint, jsonify, request, make_response
from core import db, app
from core.models.user_model import User
from flask_jwt_extended import create_access_token, create_refresh_token
user_ctrl = Blueprint('user', __name__)

@user_ctrl.route('/login', methods=['POST'])
def login():
    '''
        Accepts objects like:
            {
                "authorization": {
                    "name": "Morty",
                    "password": "229"
                }
            }
    '''
    auth = request.get_json()
    auth = auth['authorization']

    user = User.objects(name=auth['name']).first()
    if user and user.verify_hash(auth['password'], user.password):

        access_token = create_access_token(identity=auth['name'])
        refresh_token = create_refresh_token(identity=auth['name'])
        return make_response(jsonify({
            "message": "Logged in as {}".format(user.name),
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200)

    return make_response(jsonify({'message': 'Incorrect login or password!'}), 400)

@user_ctrl.route('/new', methods=['POST'])
def new():
    '''
         Accepts objects like:
            {
                "authorization": {
                    "name": "Morty",
                    "password": "229",
                    "confirm_password": "229"
                }
            }
    '''
    try:
        req_data = request.get_json()
        req_data = req_data['authorization']
        if User.objects(name=req_data['name']).first():
            raise ValueError(jsonify({'message': 'User {} already exists'.format(req_data['name'])}))

        if (len(req_data['password']) > 20):
            raise ValueError(jsonify({'message': 'Password too long!'}))

        if req_data['password'] == req_data['confirm_password'] :
            user_object = User()
            user_object.name = req_data['name']
            user_object.password = User.generate_hash(req_data['password'])
            user_object.actions_performed = 0
            user_object.save()
            return make_response(jsonify({ 'message': 'Done!' }), 201)
        else:
            raise ValueError('Passowrd and confirmatiom dont match')

    except BaseException as e:
        return make_response(jsonify({'message': str(e)}), 400)