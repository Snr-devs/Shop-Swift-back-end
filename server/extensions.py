from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_JWT_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter_util import get_remote_address

db= SQLAlchemy()
migrate=Migrate()
jwt=JWTManager()
ma=Marshmallow()
limiter=Limiter()