
🛠️ MVP Features for Your Backend
1. User Management (Optional for now, but useful later)
✅ Register user

✅ Login user

✅ View user profile

👉 If your assignment doesn’t require auth, you can skip or fake user IDs for now.

2. Products
✅ List all products (GET /products)

✅ View single product (GET /products/<id>)

✅ Create a product (POST /products)

✅ Update product (PUT /products/<id>)

✅ Delete product (DELETE /products/<id>)

You'll need a Product model with fields like: name, price, description, image_url, stock, etc.

3. Cart / Order
✅ Create an order (POST /orders)

Accepts a list of product IDs and quantities

✅ View orders (user's past orders) (GET /orders)

✅ View single order (GET /orders/<id>)

This can be simple: associate orders with a user (or session), total the price, and mark them as "pending" or "paid".

4. M-Pesa Integration
✅ STK Push endpoint (POST /mpesa/stkpush)

✅ Callback endpoint (POST /mpesa/callback)

✅ Verify payment (optional)

✅ Store transaction details (amount, phone, status)

You need the Daraja API (Safaricom) and the following:

Business ShortCode

Consumer Key & Secret

Passkey

🧩 Example MVP Routes
Route	Method	Description
/products	GET	List products
/products	POST	Add product
/products/<id>	GET	View product details
/orders	POST	Place an order
/orders	GET	List orders
/mpesa/stkpush	POST	Trigger M-Pesa STK push
/mpesa/callback	POST	Receive payment confirmation

⚙️ Models You'll Need
🧾 Product
id, name, price, description, image_url, stock

🛒 Order
id, user_id, products (many-to-many or JSON list), total_price, status, created_at

💰 Transaction
id, order_id, phone_number, amount, mpesa_receipt, status, timestamp