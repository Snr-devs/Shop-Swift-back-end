import pytest
from app import create_app
from server.extensions import db
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

def test_create_product(app):
    with app.app_context():
        product = Product(name='Test Product', price=25.99, stock=10, category='Books')
        db.session.add(product)
        db.session.commit()

        saved = Product.query.first()
        assert saved.name == 'Test Product'
        assert saved.stock == 10
        assert float(saved.price) == 25.99

def test_update_stock(app):
    with app.app_context():
        product = Product(name='Test Product', price=25.99, stock=5)
        db.session.add(product)
        db.session.commit()

        product.update_stock(3)
        assert product.stock == 8
