from flask import Blueprint, jsonify, request, make_response
import datetime
from core import db, app
from core.models.post_model import Post
from core.models.user_model import User
from core.models.comment_model import Comment
from flask_jwt_extended import jwt_required
from core.utils import action_limit_util as alu

comment_ctrl = Blueprint('comment', __name__)


@comment_ctrl.route('/get/<string:id>', methods=['GET'])
def get_comment(id):
    '''
    :param id: comment id
    :return: full comment
    '''
    try:
        return make_response(jsonify(Comment.objects.get(id=id)), 200)
    except BaseException as e:
        return make_response(jsonify({ 'message': str(e) }), 400)

@comment_ctrl.route('/new', methods=['PUT'])
@jwt_required
def new():
    '''
        Accepts object like:
        {
            "comment": {
                "post_id": "5b15476c36f0571774febfa9",
                "creator": "Morty",
                "text": "GET ME HOME, YOU OLD LUNATIC"
            }
        }
    '''
    try:
        req_data = request.get_json()
        req_data = req_data['comment']
        user = User.objects(name=req_data['creator']).first()
        if alu.validate_actions(user):
            current_post = Post.objects.get(id=req_data['post_id'])

            if not current_post:
                raise ValueError('Post {} not exists'.format(req_data['post_id']))

            if not user.actions_performed:
                user.actions_performed = 0

            if req_data and user.actions_performed <= 5:
                comment_object = Comment()
                comment_object.creator = req_data['creator']
                comment_object.text = req_data['text']
                comment_object.save()
                current_post.update(push__comments=comment_object.id)
                user.actions_performed += 1
                user.save()
                return make_response(jsonify({'message': 'Done!'}), 201)
        else:
            raise ValueError('You are still in cooldown')

    except BaseException as e:
        return make_response(jsonify({'message': str(e)}), 400)

