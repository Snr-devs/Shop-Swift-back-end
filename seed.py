import random
from datetime import datetime
from faker import Faker
from werkzeug.security import generate_password_hash

from server import create_app
from server.extensions import db
from server.models.user import User
from server.models.product import Product
from server.models.order import Order, OrderProduct
from server.models.comment import Comment

fake = Faker()
app = create_app()

IMAGE_LINKS = [
    "https://images.unsplash.com/photo-1542291026-7eec264c27ff?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://plus.unsplash.com/premium_photo-1719289799376-d3de0ca4ddbc?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://plus.unsplash.com/premium_photo-1719289799376-d3de0ca4ddbc?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=1099&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://images.unsplash.com/photo-1627384113743-6bd5a479fffd?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://plus.unsplash.com/premium_photo-1661597156656-75ba116e9e1d?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
    "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MzZ8fHByb2R1Y3RzfGVufDB8fDB8fHww",
    "https://images.unsplash.com/photo-1651863548695-b474e99ffcb9?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NDZ8fHByb2R1Y3RzfGVufDB8fDB8fHww",
    "https://images.unsplash.com/photo-1640890959827-6307611b34a1?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NTJ8fHByb2R1Y3RzfGVufDB8fDB8fHww",
    "https://images.unsplash.com/photo-1567102109796-90071d28cb38?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NTR8fHByb2R1Y3RzfGVufDB8fDB8fHww",
    "https://plus.unsplash.com/premium_photo-1677526496597-aa0f49053ce2?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NzN8fHByb2R1Y3RzfGVufDB8fDB8fHww",
    "https://images.unsplash.com/photo-1569529465841-dfecdab7503b?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fGFsY29ob2x8ZW58MHx8MHx8fDA%3D",
    "https://images.unsplash.com/photo-1618885472179-5e474019f2a9?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fGFsY29ob2x8ZW58MHx8MHx8fDA%3D",
    "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8Y3VwfGVufDB8fDB8fHww",
]

def reset_db():
    """Drop and recreate all tables."""
    db.drop_all()
    db.create_all()

def seed_products():
    products = []
    for i in range(15):
        product = Product(
            name=fake.word().title() + f" #{i+1}",
            description=fake.sentence(nb_words=12),
            price=round(random.uniform(5, 150), 2),
            image_url=IMAGE_LINKS[i]
        )
        db.session.add(product)
        products.append(product)
    db.session.commit()
    return products

def seed_users():
    data = [("alice", "alice@gmail.com"), ("linus", "linus@gmail.com")]
    for username, email in data:
        db.session.add(
            User(
                username=username,
                email=email,
                password=generate_password_hash("password123"),
                phone_number=f"+2547{random.randint(10000000, 99999999)}"
            )
        )
    db.session.commit()

def run_seed():
    with app.app_context():
        reset_db()
        seed_products()
        seed_users()
        print("🌱 Seeded 15 products & 2 users (orders/comments left empty).")

if __name__ == "__main__":
    run_seed()
