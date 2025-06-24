from app.extensions import db
from werkzeug.security import generate_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime,)
    updated_at = db.Column(db.DateTime,onupdate=db.func.now())

    def __init__(self, username, email, password, phone_number=None):
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.set_password(password)

    def set_password(self, password):
       
        self.password_hash = generate_password_hash(password)


    def __repr__(self):
        return f'<User {self.username}>'