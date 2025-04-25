from flask import Blueprint, request, jsonify
from app import db
from app.models import Order

order_bp = Blueprint('order', __name__)

@order_bp.route('/', methods=['POST'])
def create_order():
    data = request.json
    order = Order(
        car_id=data['car_id'],
        buyer_id=data['buyer_id'],
    )
    db.session.add(order)
    db.session.commit()
    return jsonify({'message': 'Order created successfully'})

@order_bp.route('/<int:user_id>', methods=['GET'])
def get_orders(user_id):
    orders = Order.query.filter_by(buyer_id=user_id).all()
    return jsonify([{
        'id': order.id,
        'car_id': order.car_id,
        'status': order.status,
        'created_at': order.created_at
    } for order in orders])
