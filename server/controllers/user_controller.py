from flask import Blueprint, make_response
from server.models.user import User
from server.schemas.user_schema import user_schema, users_schema

user_bp = Blueprint('users', __name__)


@user_bp.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return make_response(user_schema.dump(user), 200)


@user_bp.route('/api/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return make_response(users_schema.dump(users), 200)
