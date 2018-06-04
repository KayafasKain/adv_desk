from flask import Blueprint, jsonify, request, make_response
import datetime
from core import db, app
from core.models.post_model import Post
from core.models.user_model import User
from flask_jwt_extended import jwt_required
from core.utils import action_limit_util as alu
post_ctrl = Blueprint('post', __name__)

@post_ctrl.route('/get', methods=['GET'])
def get_posts():
    '''
    :return: all advertisments
    '''
    try:
        return make_response(jsonify({ 'posts': Post.objects().all()}), 200)
    except BaseException as e:
        return make_response(jsonify({'message': str(e)}), 400)

@post_ctrl.route('/get/<string:slug>', methods=['GET'])
def get_post(slug):
    '''
    :param slug:
    :return: full advertisment
    '''
    try:
        return make_response(jsonify(Post.objects(slug=slug).first()), 200)
    except BaseException as e:
        return make_response(jsonify({'message': str(e)}), 400)

@post_ctrl.route('/rate/get/<string:post_id>', methods=['GET'])
def get_rate(post_id):
    '''
    :param post_id: current post id
    :return:    {
                    "rates": [
                        {
                            "rate": 5,
                            "user_id": "5b1508db36f0572bd859f291"
                        }
                    ]
                }
    '''
    try:
        current_post = Post.objects.get(id=post_id)
        return make_response(jsonify({'rates': current_post.rates }), 200)
    except BaseException as e:
        return make_response(jsonify({'message': str(e)}), 400)

@post_ctrl.route('/rate', methods=['PUT'])
@jwt_required
def rate():
    '''
        Accepts object like:
        {
            "post": {
                "post_id": "5b153d2236f0572e345d63f3",
                "user_id": "5b1508db36f0572bd859f291",
                "rate": 5
            }
        }
    '''
    try:
        req_data = request.get_json()
        req_data = req_data['post']
        current_post = Post.objects.get(id=req_data['post_id'])
        user = User.objects.get(id=req_data['user_id'])
        if alu.validate_actions(user):
            current_post.update(push__rates={
                "user_id": req_data['user_id'],
                "rate": req_data['rate']
            })

            user.actions_performed += 1
            user.save()
            return make_response(jsonify({'message': 'success!'}), 200)
        else:
            raise ValueError('You are still in cooldown')

    except BaseException as e:
        return make_response(jsonify({'message': str(e)}), 400)

@post_ctrl.route('/new', methods=['POST'])
@jwt_required
def new():
    '''
        Make new advertisment
        Accepts objects like:
        {
            "post": {
                "slug": "i-am-in-space",
                "creator": "Morty",
                "title": "Get me out of here, RICK!1"
            }
        }
    '''
    try:
        req_data = request.get_json()
        req_data = req_data['post']
        user = User.objects(name=req_data['creator']).first()

        if alu.validate_actions(user):
            if Post.objects(slug=req_data['slug']).first():
                raise ValueError('Slug {} already exists'.format(req_data['slug']))

            if not user.actions_performed:
                user.actions_performed = 0

            if req_data and user.actions_performed <= 5:
                post_object = Post()
                post_object.slug = req_data['slug']
                post_object.creator = req_data['creator']
                post_object.title = req_data['title']
                post_object.created_at = datetime.datetime.utcnow()
                post_object.rate = 0
                post_object.save()
                user.actions_performed += 1
                user.save()

                return make_response(jsonify({'message': 'Done!'}), 201)
        else:
            raise ValueError('You are still in cooldown')
    except BaseException as e:
        return make_response(jsonify({'message': str(e)}), 400)

