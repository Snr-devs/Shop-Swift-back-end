import random
from faker import Faker
from server import create_app
from server.extensions import db
from server.models.user import User
from server.models.product import Product
# from server.models.order import Order, OrderProduct
# from server.models.comment import Comment

fake = Faker()
app = create_app()

IMAGE_LINKS = [
    "https://images.unsplash.com/photo-1542291026-7eec264c27ff?q=80&w=1170&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?q=80&w=1170&auto=format&fit=crop",
    "https://plus.unsplash.com/premium_photo-1719289799376-d3de0ca4ddbc?q=80&w=1170&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=1099&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1627384113743-6bd5a479fffd?q=80&w=1170&auto=format&fit=crop",
    "https://plus.unsplash.com/premium_photo-1661597156656-75ba116e9e1d?q=80&w=687&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=500&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1651863548695-b474e99ffcb9?w=500&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1640890959827-6307611b34a1?w=500&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1567102109796-90071d28cb38?w=500&auto=format&fit=crop",
    "https://plus.unsplash.com/premium_photo-1677526496597-aa0f49053ce2?w=500&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1569529465841-dfecdab7503b?w=500&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1618885472179-5e474019f2a9?w=500&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=500&auto=format&fit=crop",
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
            image_url=IMAGE_LINKS[i % len(IMAGE_LINKS)]
        )
        db.session.add(product)
        products.append(product)
    db.session.commit()
    return products

def seed_users():
    users_data = [
        {"username": "alice", "email": "alice@gmail.com", "password": "alicepass"},
        {"username": "linus", "email": "linus@gmail.com", "password": "linuspass"},
    ]

    for user in users_data:
        seeded_user = User(
            username=user["username"],
            email=user["email"],
            password=user["password"],
            phone_number=f"+2547{random.randint(10000000, 99999999)}"
        )
        db.session.add(seeded_user)

    db.session.commit()


def run_seed():
    with app.app_context():
        reset_db()
        seed_products()
        seed_users()
        print("🌱 Seeded 15 products & 2 users (orders/comments left empty).")

if __name__ == "__main__":
    run_seed()
