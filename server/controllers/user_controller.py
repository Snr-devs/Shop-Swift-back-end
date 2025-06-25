vfrom flask import Blueprint, request, make_response, jsonify
from .models.user import User
from .extensions import db
from .schemas.user_schema import user_schema, users_schema
from werkzeug.security import generate_password_hash, check_password_hash


user_bp = Blueprint('users', __name__)


@user_bp.route('/users', methods=['POST'])
def register_user():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    phone_number = data.get('phone_number')
    password = data.get('password')

    if not username or not email or not password:
        return make_response({'error': 'Username, email, and password are required'}, 400)

    if User.query.filter_by(email=email).first():
        return make_response({'error': 'Email already in use'}, 409)

    if User.query.filter_by(username=username).first():
        return make_response({'error': 'Username already taken'}, 409)

    
    hashed_password = generate_password_hash(password)

    new_user = User(username=username, email=email, password=hashed_password, phone_number=phone_number)
    db.session.add(new_user)
    db.session.commit()

    response_data = user_schema.dump(new_user)
    return make_response(response_data, 201)


@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    response_data = user_schema.dump(user)
    return make_response(response_data, 200)


@user_bp.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    response_data = users_schema.dump(users)
    return make_response(response_data, 200)
