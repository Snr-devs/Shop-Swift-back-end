from flask import Blueprint, request, make_response, jsonify
from .extensions import db
from .models.comment import Comment
from .models.user import User
from .models.product import Product
from .schemas.comment_schema import CommentSchema

comment_bp = Blueprint('comments', __name__)
comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)


@comment_bp.route('/comments', methods=['POST'])
def create_comment():
    data = request.get_json()

    content = data.get('content')
    user_id = data.get('user_id')
    product_id = data.get('product_id')

    if not content or not user_id or not product_id:
        return make_response({'error': 'Missing content, user_id, or product_id'}, 400)

    
    user = User.query.get(user_id)
    product = Product.query.get(product_id)
    if not user or not product:
        return make_response({'error': 'User or Product not found'}, 404)

    comment = Comment(content=content, user_id=user_id, product_id=product_id)
    db.session.add(comment)
    db.session.commit()

    return make_response(comment_schema.dump(comment), 201)


@comment_bp.route('/comments', methods=['GET'])
def get_comments():
    comments = Comment.query.all()
    return make_response(comments_schema.dump(comments), 200)


@comment_bp.route('/comments/<int:id>', methods=['GET'])
def get_comment(id):
    comment = Comment.query.get_or_404(id)
    return make_response(comment_schema.dump(comment), 200)


@comment_bp.route('/comments/<int:id>', methods=['DELETE'])
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    return make_response({'message': 'Comment deleted'}, 200)
