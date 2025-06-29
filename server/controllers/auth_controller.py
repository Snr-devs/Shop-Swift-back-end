from flask import Blueprint, request, make_response
from werkzeug.security import check_password_hash
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from datetime import timedelta

from server.models.user import User
from server.extensions import db, limiter
from server.schemas.user_schema import UserSchema
from server.utils.token import generate_tokens

auth_bp = Blueprint('auth', __name__)
user_schema = UserSchema()


@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    phone_number = data.get('phone_number')

    if not username or not email or not password:
        return make_response({'error': 'Missing required fields'}, 400)

    if User.query.filter((User.email == email) | (User.username == username)).first():
        return make_response({'error': 'User already exists'}, 409)

    user = User(username=username, email=email, password=password, phone_number=phone_number)

    db.session.add(user)
    db.session.commit()

    return make_response(user_schema.dump(user), 201)


@auth_bp.route('/api/login', methods=['POST'])
@limiter.limit("3 per minute")
def login():
    data = request.get_json()

    identifier = data.get("username") or data.get("email")
    password = data.get("password")

    if not identifier or not password:
        return make_response({'error': 'Missing credentials'}, 400)

    user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()

    if not user or not check_password_hash(user.password_hash, password):
        return make_response({'error': 'Invalid credentials'}, 401)

    tokens = generate_tokens(user)

    return make_response({
        'message': 'Login successful',
        **tokens,
        'user': user_schema.dump(user)
    }, 200)


@auth_bp.route('/api/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return make_response(user_schema.dump(user), 200)


@auth_bp.route('/api/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)

    data = request.get_json()
    new_email = data.get('email', user.email)

    if new_email != user.email:
        if User.query.filter(User.email == new_email, User.id != user.id).first():
            return make_response({'error': 'Email already in use'}, 409)

    user.username = data.get('username', user.username)
    user.email = new_email
    user.phone_number = data.get('phone_number', user.phone_number)

    db.session.commit()
    return make_response(user_schema.dump(user), 200)


@auth_bp.route('/api/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    new_access_token = generate_tokens(user_id)['access_token']
    return make_response({'access_token': new_access_token}, 200)
