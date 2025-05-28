from marshmallow import fields,Schema
class NewsLetterSchema(Schema):
    news_letter_id=fields.UUID(dump_only=True)
    name=fields.String(required=True)
    email=fields.String(required=True)
    subject=fields.String(required=True)
    content=fields.String(required=True)
    created_at=fields.DateTime(dump_only=True)