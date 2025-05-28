from marshmallow import Schema,fields
from marshmallow.validate import Length,OneOf
from utils.enums import Gender,Role

class UserSchema(Schema):
    user_id=fields.UUID(dump_only=True)
    user_name=fields.String(required=True,validate=Length(min=3,max=50))
    user_email=fields.Email(required=True)
    user_mobile=fields.String(required=False)
    user_password=fields.String(required=False,load_only=True)
    user_gender = fields.String(validate=OneOf([g.value for g in Gender]), allow_none=True)
    user_role = fields.String(required=False, validate=OneOf([r.value for r in Role]))
    is_deleted=fields.Boolean(dump_default=False)
    created_at=fields.DateTime(dump_only=True)
    updated_at=fields.DateTime(dump_only=True)
8 