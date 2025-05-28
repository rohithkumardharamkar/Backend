from marshmallow import fields,Schema
class Scholarships(Schema):
    scholarship_id=fields.UUID(dump_only=True)
    ngo_id=fields.UUID(required=True)
    user_id=fields.UUID(required=True)
    approved=fields.Boolean(dump_default=False)
    reason=fields.String(allow_none=True)
    is_deleted=fields.Boolean(dump_default=False)
    created_at=fields.DateTime(dump_only=True)
    updated_at=fields.DateTime(dump_only=True)

