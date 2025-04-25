from flask import Blueprint, request, jsonify
from app import db
from app.models import Car

car_bp = Blueprint('car', __name__)

@car_bp.route('/', methods=['GET'])
def get_cars():
    query = Car.query
    brand = request.args.get('brand')
    model = request.args.get('model')
    condition = request.args.get('condition')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)

    if brand:
        query = query.filter(Car.brand.ilike(f'%{brand}%'))
    if model:
        query = query.filter(Car.model.ilike(f'%{model}%'))
    if condition:
        query = query.filter(Car.condition == condition)
    if min_price is not None:
        query = query.filter(Car.price >= min_price)
    if max_price is not None:
        query = query.filter(Car.price <= max_price)

    cars = query.all()
    return jsonify([{
        'id': car.id,
        'brand': car.brand,
        'model': car.model,
        'year': car.year,
        'price': car.price,
        'condition': car.condition,
        'description': car.description,
        'image_url': car.image_url,
        'is_sold': car.is_sold
    } for car in cars])

@car_bp.route('/', methods=['POST'])
def add_car():
    data = request.json
    new_car = Car(
        brand=data['brand'],
        model=data['model'],
        year=data['year'],
        price=data['price'],
        description=data.get('description', ''),
        image_url=data.get('image_url', ''),
        condition=data.get('condition', 'used'),
        user_id=data['user_id']
    )
    db.session.add(new_car)
    db.session.commit()
    return jsonify({'message': 'Car added successfully'})
