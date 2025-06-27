from marshamallow import Schema, fields, ValidationError

class OrderProductSchema(Schema):
    id = fields.Int(dump_only=True)
    order_id = fields.Int(required=True)
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True)
    price = fields.Decimal(as_string=True, dump_only=True)  

    @validates('quantity')
    def validate_quantity(self, value):
        if value < 1:
            raise ValidationError("Quantity must be at least 1.")
        
class OrderSchema(Schema):
    id=fields.Int(dump_only=True)
    user_id=fields.Int(dump_only=True)
    total_price=fields.Decimal(as_string=True, dump_only=True)
    status=fields.Str(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    order_products = fields.Nested(OrderProductSchema, many=True, required=True)


order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

order_product_schema = OrderProductSchema()
order_products_schema = OrderProductSchema(many=True)