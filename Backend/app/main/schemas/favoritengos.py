from marshmallow import Schema,fields
class FavNgoSchema(Schema):
    favorite_id=fields.UUID(dump_only=True)
    ngo_id=fields.UUID(required=True)
    user_id=fields.UUID(required=True)
    is_deleted=fields.Boolean(dump_default=False)
    created_at=fields.DateTime(dump_only=True)
    updated_at=fields.DateTime(dump_only=True)