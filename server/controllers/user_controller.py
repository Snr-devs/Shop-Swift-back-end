from flask import Blueprint, request, make_response
from server.models.user import User
from server.extensions import db, limiter
from server.schemas.user_schema import user_schema, users_schema
from werkzeug.security import check_password_hash
from server.utils.token import generate_tokens
from sqlalchemy import or_

user_bp = Blueprint('users', __name__)

@user_bp.route('/register', methods=['POST'])
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

    # ✅ Just pass plain password. Model will hash it.
    new_user = User(username=username, email=email, password=password, phone_number=phone_number)
    db.session.add(new_user)
    db.session.commit()

    response_data = {**generate_tokens(new_user), **user_schema.dump(new_user)}
    return make_response(response_data, 201)

@user_bp.route("/login", methods=['POST'])
@limiter.limit("3 per minute")
def login_user():
    data = request.get_json()

    identifier = data.get("username") or data.get("email")
    password = data.get("password")

    if not identifier or not password:
        return make_response({"error": "Username/email and password are required"}, 400)

    user = User.query.filter(
        or_(User.username == identifier, User.email == identifier)
    ).first()

    if not user or not check_password_hash(user.password_hash, password):
        return make_response({"error": "Invalid username/email or password"}, 401)

    response = {**generate_tokens(user), "user": user_schema.dump(user)}
    return make_response(response, 200)

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return make_response(user_schema.dump(user), 200)

@user_bp.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return make_response(users_schema.dump(users), 200)
