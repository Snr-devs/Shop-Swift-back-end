from server.extensions import db
from datetime import datetime

class Search(db.Model):
    __tablename__ = 'searches'

    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='searches')

    def __repr__(self):
        return f'<Search query="{self.query}" by User {self.user_id}>'
