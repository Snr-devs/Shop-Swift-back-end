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
    "https://www.freepik.com/premium-photo/kitchen-appliances-blender-toaster-coffee-machine-meat-ginder-microwave-oven-kettle-3d_18349428.htm#fromView=search&page=1&position=13&uuid=bc30d18d-3c0d-4f91-ba24-d87a36f9cb7c&query=appliances",
    "https://www.freepik.com/premium-photo/home-appliances-gas-cooker-tv-cinema-refrigerator-air-conditioner-microwave-laptop-washing-machine_9109577.htm#fromView=search&page=1&position=20&uuid=bc30d18d-3c0d-4f91-ba24-d87a36f9cb7c&query=appliances",
    "https://www.freepik.com/free-photo/view-electronic-product-balancing-podium_38672769.htm#fromView=search&page=1&position=21&uuid=bc30d18d-3c0d-4f91-ba24-d87a36f9cb7c&query=appliances",
    "https://www.freepik.com/free-photo/new-iron-isolated-white-background_21064720.htm#fromView=search&page=1&position=24&uuid=bc30d18d-3c0d-4f91-ba24-d87a36f9cb7c&query=appliances",
    "https://www.freepik.com/free-photo/refrigerator-surrounded-by-nature-scene_38048683.htm#fromView=search&page=1&position=27&uuid=bc30d18d-3c0d-4f91-ba24-d87a36f9cb7c&query=appliances",
    "https://www.freepik.com/free-vector/smart-fridge-gas-oven-hood-kitchen-appliances_9396052.htm#fromView=search&page=1&position=5&uuid=ae0676c8-7e75-4c72-9fd6-edbb087eb2ee&query=appliances",
    "https://www.freepik.com/free-photo/small-plant-near-various-cosmetics-bottles_2146565.htm#fromView=search&page=1&position=0&uuid=1f09890a-7214-4c0a-8711-2fdc0e5c36ab&query=toiletries",
    "https://www.freepik.com/premium-photo/hotel-amenities-kit-table-beige-background_42837545.htm#fromView=search&page=1&position=19&uuid=1f09890a-7214-4c0a-8711-2fdc0e5c36ab&query=toiletries",
    "https://www.freepik.com/premium-photo/set-care-body-isolated-white_16331229.htm#fromView=search&page=1&position=29&uuid=1f09890a-7214-4c0a-8711-2fdc0e5c36ab&query=toiletries",
    "https://www.freepik.com/free-photo/coconuts-plant-cones_1454710.htm#fromView=search&page=1&position=24&uuid=1f09890a-7214-4c0a-8711-2fdc0e5c36ab&query=toiletries",
    "https://www.freepik.com/free-photo/high-angle-eco-friendly-products-composition_26471429.htm#fromView=search&page=1&position=44&uuid=1f09890a-7214-4c0a-8711-2fdc0e5c36ab&query=toiletries",
    "https://www.freepik.com/premium-photo/beauty-set-gift-isolated-white_222550110.htm#fromView=search&page=1&position=24&uuid=553c8c71-65c7-4b62-bd8e-bab3338bb665&query=beauty+producuts",
    "https://www.freepik.com/free-photo/makeup-lipstick_4166641.htm#fromView=search&page=1&position=17&uuid=553c8c71-65c7-4b62-bd8e-bab3338bb665&query=beauty+producuts",
    "https://www.freepik.com/free-vector/red-cosmetic-line-skin-care-makeup_8502334.htm#fromView=search&page=1&position=36&uuid=553c8c71-65c7-4b62-bd8e-bab3338bb665&query=beauty+producuts",
    "https://www.freepik.com/free-photo/still-life-skincare-products_25218968.htm#fromView=search&page=1&position=0&uuid=553c8c71-65c7-4b62-bd8e-bab3338bb665&query=beauty+producuts",
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
