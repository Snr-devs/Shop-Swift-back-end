from flask import Blueprint, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from server.extensions import db
from server.models.user import User
from server.schemas.user_schema import UserSchema

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)

from datetime import timedelta

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

    password_hash = generate_password_hash(password)
    user = User(username=username, email=email, phone_number=phone_number, password_hash=password_hash)

    db.session.add(user)
    db.session.commit()

    return make_response(user_schema.dump(user), 201)



@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return make_response({'error': 'Missing email or password'}, 400)

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return make_response({'error': 'Invalid credentials'}, 401)

    access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
    refresh_token = create_refresh_token(identity=user.id)

    return make_response({
        'message': 'Login successful',
        'access_token': access_token,
        'refresh_token': refresh_token,
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
    new_access_token = create_access_token(identity=user_id)
    return make_response({'access_token': new_access_token}, 200)
