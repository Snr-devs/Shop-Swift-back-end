import pytest
from app import create_app
from server.extensions import db
from models.order import Order, OrderProduct
from models.user import User
from models.product import Product

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_order_with_product(app):
    with app.app_context():
        user = User(username="testuser", email="test@example.com", password="testpass")
        product = Product(name="Book", price=10.00, stock=5)
        db.session.add_all([user, product])
        db.session.commit()

        order = Order(user_id=user.id, total_price=10.00)
        db.session.add(order)
        db.session.flush() 
        order_item = OrderProduct(order_id=order.id, product_id=product.id, quantity=1, price=10.00)
        db.session.add(order_item)
        db.session.commit()

        saved_order = Order.query.first()
        saved_product = saved_order.order_products[0]

        assert saved_order.user_id == user.id
        assert saved_product.product_id == product.id
        assert saved_product.quantity == 1
        assert float(saved_product.price) == 10.00
