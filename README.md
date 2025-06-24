💡 OVERALL STRUCTURE OF MVP FEATURES
🧱 Feature	🎯 What It Does
User	Register / Get user
Product	Add / View / Update / Delete products
Order	Place order / View order(s)
M-Pesa	Initiate STK Push / Receive callback

✅ 1. User MVP
Purpose: Register and fetch user info (optional login logic).

🔧 Model: User
id, username, email, phone_number, password (hashed or plain for now)

📦 Routes:
Method	Route	Purpose
POST	/users	Register user
GET	/users/<id>	View user profile

✅ 2. Product MVP
Purpose: Admin or seller can manage products; users can view products.

🔧 Model: Product
id, name, price, description, stock, image_url

📦 Routes:
Method	Route	Purpose
GET	/products	List all products
GET	/products/<id>	View single product
POST	/products	Add new product
PUT	/products/<id>	Update product
DELETE	/products/<id>	Delete product

✅ 3. Order MVP
Purpose: Allow a user to place an order and view order(s).

🔧 Model: Order
id, user_id, products (JSON or many-to-many), total_price, status, created_at

📦 Routes:
Method	Route	Purpose
POST	/orders	Place an order
GET	/orders	View all user orders
GET	/orders/<id>	View a specific order

✅ 4. M-Pesa MVP (STK Push)
Purpose: Allow user to pay via M-Pesa on order.

🔧 Model: Transaction
id, order_id, amount, phone_number, mpesa_receipt, status, timestamp

📦 Routes:
Method	Route	Purpose
POST	/mpesa/stkpush	Start STK Push
POST	/mpesa/callback	Receive callback from Safaricom
GET	/transactions	View all payment attempts (optional)

📁 Suggested Folder Layout (with only controllers/)
pgsql
Copy
Edit
ecommerce_app/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── order.py
│   │   └── transaction.py
│   ├── controllers/
│   │   ├── user_controller.py
│   │   ├── product_controller.py
│   │   ├── order_controller.py
│   │   └── mpesa_controller.py
│   ├── schemas/
│   └── utils/
│       └── mpesa_client.py
├── manage.py
├── requirements.txt
├── .env
└── README.md
