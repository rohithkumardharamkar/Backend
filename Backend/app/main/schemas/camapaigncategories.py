from marshmallow import Schema,fields
class CampaignCategorySchema(Schema):
    category_id=fields.UUID(dump_only=True)
    category_name=fields.String(required=True)
    is_deleted=fields.String(dump_default=False)
    created_at=fields.Boolean(dump_only=True)
    updated_at=fields.Boolean(dump_only=True)
