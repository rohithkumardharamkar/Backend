from marshmallow import fields,Schema
from marshmallow.validate import Length,OneOf
from utils.enums import Status
class NgoSchema(Schema):
    ngo_id=fields.UUID(required=True)
    ngo_name=fields.String(required=True)
    ngo_mission=fields.String(required=True)
    ngo_status=fields.String(validate=OneOf([e.value for e in Status]),allow_none=True)
    ngo_location=fields.String(allow_none=True)
    user_id=fields.UUID(required=True)
    ngo_blacklisted=fields.Boolean(dump_default=False)
    is_deleted=fields.Boolean(dump_default=False)
    is_verified=fields.Boolean(dump_default=False)
    created_at=fields.DateTime(dump_only=True)
    updated_at=fields.DateTime(dump_only=True)

