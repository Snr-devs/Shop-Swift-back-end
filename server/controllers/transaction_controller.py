from flask import Blueprint, request, make_response, jsonify
from .extensions import db
from .models.transaction import Transaction
from .models.order import Order
from .schemas.transaction_schema import TransactionSchema
from datetime import datetime

mpesa_bp = Blueprint('mpesa', __name__)
transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)

@mpesa_bp.route('/mpesa', methods=['POST'])
def initiate_mpesa():
    data = request.get_json()
    order_id = data.get('order_id')
    phone_number = data.get('phone_number')
    amount = data.get('amount')

    if not order_id or not phone_number or not amount:
        return make_response({'error': 'Missing required fields'}, 400)

    order = Order.query.get(order_id)
    if not order:
        return make_response({'error': 'Order not found'}, 404)

    transaction = Transaction(
        order_id=order_id,
        phone_number=phone_number,
        amount=amount,
        status='initiated',
        timestamp=datetime.utcnow()
    )

    db.session.add(transaction)
    db.session.commit()

    response_data = transaction_schema.dump(transaction)
    return make_response(response_data, 201)


@mpesa_bp.route('/mpesa/callback', methods=['POST'])
def mpesa_callback():
    data = request.get_json()

    receipt_number = data.get('mpesa_receipt')
    transaction_id = data.get('transaction_id')
    status = data.get('status', 'completed')

    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        return make_response({'error': 'Transaction not found'}, 404)

    transaction.mpesa_receipt = receipt_number
    transaction.status = status
    db.session.commit()

    return make_response({'message': 'Callback processed'}, 200)


@mpesa_bp.route('/transactions', methods=['GET'])
def list_transactions():
    transactions = Transaction.query.all()
    result = transactions_schema.dump(transactions)
    return make_response(result, 200)
