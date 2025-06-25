from flask import Blueprint, request, make_response
from .models.product import Product
from .extensions import db
from .schemas.product_schema import ProductSchema

product_bp = Blueprint('products', __name__)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


@product_bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    
    name = data.get('name')
    price = data.get('price')
    if not name or not price:
        return make_response({'error': 'Name and price are required.'}, 400)
    
    product = Product(
        name=name,
        price=price,
        description=data.get('description'),
        stock=data.get('stock', 0),
        image_url=data.get('image_url'),
        category=data.get('category')
    )
    db.session.add(product)
    db.session.commit()
    
    return make_response(product_schema.dump(product), 201)



@product_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return make_response(products_schema.dump(products), 200)



@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return make_response({'error': 'Product not found'}, 404)
    
    return make_response(product_schema.dump(product), 200)



@product_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return make_response({'error': 'Product not found'}, 404)
    
    data = request.get_json()
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.description = data.get('description', product.description)
    product.stock = data.get('stock', product.stock)
    product.image_url = data.get('image_url', product.image_url)
    product.category = data.get('category', product.category)
    
    db.session.commit()
    return make_response(product_schema.dump(product), 200)


@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return make_response({'error': 'Product not found'}, 404)
    
    db.session.delete(product)
    db.session.commit()
    return make_response({'message': 'Product deleted successfully'}, 200)
