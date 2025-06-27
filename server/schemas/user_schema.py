from marshmallow import Schema, fields, validate
from .comment_schema import CommentSchema
from .order_schema import OrderSchema

class UserSchema(Schema):
    id=fields.Int(dump_only=True)
    username=fields.Str(validate=validate.Length(min=5, max=24), required=True)
    email=fields.Email(required=True)
    phone_number=fields.Str(validate=validate.Regexp(r"^(?:\+|0)[0-9]{9,12}$"))
    password_harsh=fields.Str(
        required=True,
        validate=[
           validate.Length(min=8, error="Password must be at least 8 characters long."),
           validate.Regexp(r".*[\W_]", error="Password must include at least one special character."),
           validate.Regexp(r".*[0-9]", error="Password must include at least one digit."),
        ]                        
   )
    created_at=fields.DateTime(dump_only=True)
    updated_at=fields.DateTime(dump_only=True)

    orders = fields.Nested(OrderSchema, many=True, dump_only=True)
    comments = fields.Nested(CommentSchema, many=True, dump_only=True)

user_schema= UserSchema()
users_schema=UserSchema(many=True)