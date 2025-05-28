from datetime import datetime,timezone
from sqlalchemy.dialects.postgresql import UUID
from utils.initdb import db
import uuid
class Campaigns(db.Model):
    __tablename__='campaigns'
    campaign_id=db.Column(UUID(as_uuid=True),primary_key=True,nullable=False,default=uuid.uuid4)
    ngo_id=db.Column(UUID(as_uuid=True),db.ForeignKey('ngos.ngo_id'),nullable=False)
    # camapaign_category_id=db.Column(UUID(as_uuid=True),db.ForeignKey('campaign_categories.category_id'),nullable=False)
    campaign_name=db.Column(db.String(150),nullable=False)
    campaign_location=db.Column(db.String(150),nullable=False)
    campaign_description=db.Column(db.Text,nullable=False)
    campaign_urgency=db.Column(db.Boolean,default=False)
    target_amount=db.Column(db.Integer,default=0)
    c_date=db.Column(db.String,nullable=True)
    campaign_category=db.Column(db.String(50),nullable=False)
    ngo=db.relationship('NGO',backref=db.backref('campaigns',lazy=True))
    is_deleted=db.Column(db.Boolean,default=False)
    created_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc))
    updated_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc),onupdate=lambda:datetime.now(timezone.utc))