from marshmallow import Schema, fields
from .comment_schema import CommentSchema
from .order_schema import OrderProductSchema

class ProductSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str(dump_only=True)
    price=fields.Decimal(dump_only=True, as_string=True)
    description=fields.Str(dump_only=True)
    stock=fields.Int(dump_only=True)
    image_url=fields.Str(dump_only=True)
    category=fields.Str(dump_only=True)
    created_at=fields.DateTime(dump_only=True)
    updated_at=fields.DateTime(dump_only=True)

    order_items=fields.Nested(OrderProductSchema, many=True, dump_only=True)
    comments=fields.Nested(CommentSchema, many=True, dump_only=True)


product_schema=ProductSchema()
product_list_schema=ProductSchema(many=True)
