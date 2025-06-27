from marshmallow import Schema, fields, pre_load

class CommentSchema(Schema):
    id=fields.Int(dump_only=True)
    content=fields.Str(required=True,)

    user_id=fields.Int(dump_only=True)
    product_id=fields.Int(dump_only=True)

    user=fields.Str(dump_only=True)
    product=fields.Str(dump_only=True)

    @pre_load
    def truncate_words(self, data, **kwargs):
        if 'content' in data:
            words = data['content'].strip().split()
            if len(words) > 200:
                data['content'] = ' '.join(words[:200])
        return data

comment_schema=CommentSchema()

comments_schema=CommentSchema(many=True)