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
    "hhttps://images.unsplash.com/photo-1542291026-7eec264c27ff?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
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

COMMENTS = [
    "This product exceeded my expectations!",
    "Arrived late but still worth it.",
    "Color was slightly off from the picture.",
    "Great value for the price.",
    "I`d definitely buy this again.",
    "Packaging was neat and secure.",
    "Didn`t work for me, sadly.",
    "Customer service was super helpful.",
    "My kids love it!",
    "Exactly what I needed, thank you.",
    "It`s okay — not the best, not the worst."
]

def reset_db():
    db.drop_all()
    db.create_all()

def seed_products():
    products = []
    for i in range(15):
        p = Product(
            name=fake.word().title() + f" #{i+1}",
            description=fake.sentence(nb_words=12),
            price=round(random.uniform(5, 150), 2),
            image_url=IMAGE_LINKS[i]
        )
        db.session.add(p)
        products.append(p)
    db.session.commit()
    return products

def seed_users():
    users = []
    template = [("alice", "alice@gmail.com"), ("linus", "linus@gmail.com"), ("carol", "carol@gmail.com")]
    for username, email in template:
        u = User(
            username=username,
            email=email,
            password=generate_password_hash("password123"),
            phone_number=f"+2547{random.randint(10000000, 99999999)}"
        )
        db.session.add(u)
        users.append(u)
    db.session.commit()
    return users

def create_order(user, products):
    order = Order(user_id=user.id, total_price=0, status="pending")
    db.session.add(order)
    db.session.flush()
    total = 0
    for prod in random.sample(products, random.randint(1, 4)):
        qty = random.randint(1, 3)
        db.session.add(OrderProduct(order_id=order.id, product_id=prod.id, quantity=qty, price=prod.price))
        total += prod.price * qty
    order.total_price = total
    order.status = "success"
    db.session.commit()

def create_comment(user, product, content):
    db.session.add(Comment(
        user_id=user.id,
        product_id=product.id,
        content=content,
        created_at=datetime.utcnow()
    ))

def seed_orders_and_comments(users, products):
    # User 1: 2 orders, 4 comments
    for _ in range(2):
        create_order(users[0], products)
    for comment_text, prod in zip(COMMENTS[:4], random.sample(products, 4)):
        create_comment(users[0], prod, comment_text)

    # User 2: 1 order, 2 comments
    create_order(users[1], products)
    for comment_text, prod in zip(COMMENTS[4:6], random.sample(products, 2)):
        create_comment(users[1], prod, comment_text)

    # User 3: 0 orders, 5 comments
    for comment_text, prod in zip(COMMENTS[6:11], random.sample(products, 5)):
        create_comment(users[2], prod, comment_text)

    db.session.commit()

def run_seed():
    with app.app_context():
        reset_db()
        products = seed_products()
        users = seed_users()
        seed_orders_and_comments(users, products)
        print("🌱 Seed data inserted successfully.")

if __name__ == "__main__":
    run_seed()
