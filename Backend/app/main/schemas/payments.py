from marshmallow import fields,Schema
class PaymentSchema(Schema):
    payment_id=fields.UUID(dump_only=True)
    user_id=fields.UUID(required=True)
    campaign_id=fields.UUID(required=True)
    amount=fields.Integer(required=True)
    payment_type=fields.Integer(required=True)
    created_at=fields.DateTime(dump_only=True)
    updated_at=fields.DateTime(dump_only=True)
