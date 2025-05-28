from marshmallow import fields,Schema
class LikeSchema(Schema):
    liked_id=fields.UUID(dump_only=True)
    campaign_id=fields.UUID(required=True)
    user_id=fields.UUID(required=True)
    is_liked=fields.Boolean(dump_default=False)
    is_deleted=fields.Boolean(dump_default=False)
    created_at=fields.DateTime(dump_only=True)
    updated_at=fields.DateTime(dump_only=True)