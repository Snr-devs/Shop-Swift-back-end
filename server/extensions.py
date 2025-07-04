from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from server.utils.limiter import get_remote_address

db= SQLAlchemy()
migrate=Migrate()
jwt=JWTManager()
ma=Marshmallow()
limiter=Limiter(key_func=get_remote_address)
