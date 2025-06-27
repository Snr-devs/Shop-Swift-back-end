import pytest
from datetime import datetime
from server.extensions import db
from server.models.comment import Comment
from server.models.user import User
from server.models.product import Product
from server.__init__ import create_app

@pytest.fixture
def test_app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def test_client(test_app):
    return test_app.test_client()

def test_create_comment(test_app):
    with test_app.app_context():
        
        user = User(username="testuser", email="test@example.com", password="password123")
        product = Product(name="Test Product", price=50.00, stock=10)

        db.session.add_all([user, product])
        db.session.commit()

       
        comment = Comment(content="This is a test comment", user_id=user.id, product_id=product.id)
        db.session.add(comment)
        db.session.commit()

        assert comment.id is not None
        assert comment.user_id == user.id
        assert comment.product_id == product.id
        assert comment.content == "This is a test comment"
        assert isinstance(comment.created_at, datetime)
