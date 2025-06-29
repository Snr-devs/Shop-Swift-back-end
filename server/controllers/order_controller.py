from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.models import db, Product, Order, OrderProduct

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/orders/buy', methods=['POST'])
def buy_product():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))
    user_id = get_jwt_identity()

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    if product.stock < quantity:
        return jsonify({"error": "Not enough stock"}), 400

    order = Order.query.filter_by(user_id=user_id, status='pending').first()
    if not order:
        order = Order(user_id=user_id, total_price=0)
        db.session.add(order)
        db.session.commit()

    order_product = OrderProduct.query.filter_by(order_id=order.id, product_id=product_id).first()
    if order_product:
        order_product.quantity += quantity
    else:
        order_product = OrderProduct(
            order_id=order.id,
            product_id=product.id,
            quantity=quantity,
            price=product.price
        )
        db.session.add(order_product)

    product.stock -= quantity

    order.total_price = sum([
        op.quantity * op.price for op in order.order_products
    ])

    db.session.commit()
    return jsonify({"message": "Product added to cart", "order_id": order.id}), 201


@order_bp.route('/orders/cart', methods=['GET'])
def view_cart():
    user_id = get_jwt_identity()
    order = Order.query.filter_by(user_id=user_id, status='pending').first()

    if not order or not order.order_products:
        return jsonify({
            "message": "Cart is empty",
            "cart": [],
            "total_price": "0.00"
        }), 200

    cart_items = []
    for item in order.order_products:
        product = item.product
        subtotal = item.price * item.quantity
        cart_items.append({
            "product_id": product.id,
            "name": product.name,
            "image_url": product.image_url,
            "price": str(item.price),
            "quantity": item.quantity,
            "subtotal": str(subtotal)
        })

    return jsonify({
        "order_id": order.id,
        "total_price": str(order.total_price),
        "cart": cart_items
    }), 200
@order_bp.route('/orders/cart/<int:product_id>', methods=['DELETE'])
def remove_from_cart(product_id):
    user_id = get_jwt_identity()
    order = Order.query.filter_by(user_id=user_id, status='pending').first()

    if not order:
        return jsonify({"error": "Cart not found"}), 404

    order_product = OrderProduct.query.filter_by(order_id=order.id, product_id=product_id).first()

    if not order_product:
        return jsonify({"error": "Product not in cart"}), 404

    product = order_product.product
    product.stock += order_product.quantity

    db.session.delete(order_product)

    order.total_price = sum([
        op.quantity * op.price for op in order.order_products if op.product_id != product_id
    ])

    db.session.commit()
    return jsonify({"message": f"Product {product_id} removed from cart"}), 200