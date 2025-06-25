from .extensions import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    amount = db.Column(db.Numeric, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    mpesa_receipt = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(20), default='pending')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

   
    order = db.relationship('Order', backref=db.backref('transaction', uselist=False))

    def __repr__(self):
        return f'<Transaction {self.id} - Order {self.order_id} - {self.status}>'
