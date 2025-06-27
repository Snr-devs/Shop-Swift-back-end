import pytest
from decimal import Decimal
from datetime import datetime
from server.extensions import db
from server.models.transaction import Transaction
from server.models.order import Order
from server.models.user import User
from app import create_app

@pytest.fixture
def test_app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def test_client(test_app):
    return test_app.test_client()

def test_create_transaction(test_app):
    with test_app.app_context():
     
        user = User(username="john", email="john@example.com", password="test123")
        db.session.add(user)
        db.session.commit()

      
        order = Order(user_id=user.id, total_price=Decimal("100.00"))
        db.session.add(order)
        db.session.commit()

    
        transaction = Transaction(
            order_id=order.id,
            amount=Decimal("100.00"),
            phone_number="0712345678",
            mpesa_receipt="MPESA123456",
            status="success"
        )
        db.session.add(transaction)
        db.session.commit()

        assert transaction.id is not None
        assert transaction.order_id == order.id
        assert transaction.amount == Decimal("100.00")
        assert transaction.phone_number == "0712345678"
        assert transaction.mpesa_receipt == "MPESA123456"
        assert transaction.status == "success"
        assert isinstance(transaction.timestamp, datetime)
