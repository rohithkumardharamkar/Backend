from marshmallow import Schema,fields
class BeneficairySchema(Schema):
    beneficiary_id=fields.UUID(dump_only=True)
    ngo_id=fields.UUID(required=True)
    beneficiary_name=fields.String(required=True)
    beneficiary_address=fields.String(required=True)
    is_deleted=fields.Boolean(dump_default=True)
    created_at=fields.DateTime(dump_only=True)
    updated_at=fields.DateTime(dump_only=True)