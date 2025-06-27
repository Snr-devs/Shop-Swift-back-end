# seed.py
import random
from datetime import datetime
from server.extensions import db
from server.models.user import User
from server.models.product import Product          # you must have a Product model
from server.models.order import Order, OrderProduct
from server.models.comment import Comment          # you must have a Comment model
from werkzeug.security import generate_password_hash
from faker import Faker

fake = Faker()

# ----- helper lists -----
IMAGE_LINKS = [
    "https://picsum.photos/id/1011/600/400",
    "https://picsum.photos/id/1025/600/400",
    "https://picsum.photos/id/1027/600/400",
    "https://picsum.photos/id/1035/600/400",
    "https://picsum.photos/id/1043/600/400",
    "https://picsum.photos/id/1052/600/400",
    "https://picsum.photos/id/1060/600/400",
    "https://picsum.photos/id/1074/600/400",
    "https://picsum.photos/id/1084/600/400",
    "https://picsum.photos/id/1080/600/400",
    "https://picsum.photos/id/110/600/400",
    "https://picsum.photos/id/120/600/400",
    "https://picsum.photos/id/133/600/400",
    "https://picsum.photos/id/177/600/400",
    "https://picsum.photos/id/219/600/400",
]

def reset_db():
    """Drop & create all tables (DANGER: wipes data)."""
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
        products.append(p)
        db.session.add(p)
    db.session.commit()
    return products

def seed_users():
    users = []
    template = [
        ("alice", "alice@gmail.com"),
        ("linus",   "linus@gmail.com"),
        ("carol", "carol@gmail.com"),
    ]
    for username, email in template:
        u = User(
            username=username,
            email=email,
            password=generate_password_hash("password123"),
            phone_number=f"+2547{random.randint(10000000, 99999999)}"
        )
        users.append(u)
        db.session.add(u)
    db.session.commit()
    return users

def create_order(user, products, qty=1):
    order = Order(user_id=user.id, total_price=0, status="pending")
    db.session.add(order)
    db.session.flush()  
    selected = random.sample(products, k=random.randint(1, 4))
    total = 0
    for prod in selected:
        line_qty = random.randint(1, 3)
        op = OrderProduct(
            order_id=order.id,
            product_id=prod.id,
            quantity=line_qty,
            price=prod.price
        )
        total += prod.price * line_qty
        db.session.add(op)
    order.total_price = total
    order.status = "success"
    db.session.commit()

def create_comment(user, product):
    comment = Comment(
        user_id=user.id,
        product_id=product.id,
        content=fake.sentence(nb_words=16),
        created_at=datetime.utcnow()
    )
    db.session.add(comment)

def seed_orders_and_comments(users, products):
    # User 1: 2 orders, 4 comments
    for _ in range(2):
        create_order(users[0], products)
    for prod in random.sample(products, 4):
        create_comment(users[0], prod)

    # User 2: 1 order, 2 comments
    create_order(users[1], products)
    for prod in random.sample(products, 2):
        create_comment(users[1], prod)

    # User 3: 0 orders, 5 comments
    for prod in random.sample(products, 5):
        create_comment(users[2], prod)

    db.session.commit()

def run_seed():
    reset_db()
    products = seed_products()
    users = seed_users()
    seed_orders_and_comments(users, products)
    print("🌱  Seed data inserted successfully.")

if __name__ == "__main__":
    run_seed()
