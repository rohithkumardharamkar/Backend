from marshmallow import fields,Schema
class Campaigns(Schema):
    campaign_id=fields.UUID(dump_only=True)
    ngo_id=fields.UUID(dump_only=True)
    # camapaign_category_id=fields.UUID(required=True)
    campaign_name=fields.String(required=True)
    campaign_location=fields.String(required=True)
    campaign_description=fields.String(required=True)
    campaign_urgency=fields.Boolean(dump_default=False)
    target_amount=fields.Integer(required=False)
    c_date=fields.String(required=True)
    
    is_deleted=fields.Boolean(dump_default=False)
    created_at=fields.DateTime(dump_default=False)
    updated_at=fields.DateTime(dump_default=False)