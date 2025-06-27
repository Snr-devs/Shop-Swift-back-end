from flask import Blueprint, request, make_response, jsonify
from server.models.order import Order, OrderProduct
from server.models.product import Product
from server.extensions import db
from server.schemas.order_schema import OrderSchema

order_bp = Blueprint('orders', __name__)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


@order_bp.route('/orders', methods=['POST'])
def place_order():
    data = request.get_json()

    user_id = data.get('user_id')
    products_data = data.get('products')

    if not user_id or not products_data:
        return make_response({'error': 'Missing user_id or products'}, 400)

    order = Order(user_id=user_id, total_price=0)
    total = 0

    for item in products_data:
        product = Product.query.get(item['product_id'])
        if not product:
            return make_response({'error': f'Product ID {item["product_id"]} not found'}, 404)

        quantity = item.get('quantity', 1)
        if quantity > product.stock:
            return make_response({'error': f'Not enough stock for {product.name}'}, 400)

        product.stock -= quantity

        order_product = OrderProduct(
            product_id=product.id,
            quantity=quantity,
            price=product.price * quantity
        )
        order.order_products.append(order_product)
        total += product.price * quantity

    order.total_price = total
    db.session.add(order)
    db.session.commit()

    return make_response(order_schema.dump(order), 201)


@order_bp.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return make_response(orders_schema.dump(orders), 200)


@order_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return make_response(order_schema.dump(order), 200)
