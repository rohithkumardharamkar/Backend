from utils.initdb import db
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime,timezone
import uuid
class Payments(db.Model):
    __tablename__='payments'
    payment_id=db.Column(UUID(as_uuid=True),primary_key=True,default=lambda:uuid.uuid4())
    user_id=db.Column(UUID(as_uuid=True),db.ForeignKey('users.user_id'))
    campaign_id=db.Column(UUID(as_uuid=True),db.ForeignKey('campaigns.campaign_id'))
    payment_type=db.Column(db.String,nullable=False)
    payment_amount=db.Column(db.Integer,nullable=False)
    campaign=db.relationship('Campaigns',backref=db.backref('payments',uselist=True))
    user=db.relationship('Users',backref=db.backref('payments',uselist=True))
    created_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc))
    updated_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc),onupdate=lambda:datetime.now(timezone.utc))
