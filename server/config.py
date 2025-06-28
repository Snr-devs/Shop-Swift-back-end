import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY=os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL")

    DEBUG=os.getenv("DEBUG", "False")=="True"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=7)
    RATELIMIT_HEADERS_ENABLED=True
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"sslmode": "require"}
    }