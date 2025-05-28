from datetime import datetime,timezone
from sqlalchemy.dialects.postgresql import UUID
from utils.initdb import db
import uuid


class Comments(db.Model):
    __tablename__='campaign_comments'
    comment_id=db.Column(UUID(as_uuid=True),primary_key=True,nullable=False,default=uuid.uuid4)
    campaign_id=db.Column(UUID(as_uuid=True),db.ForeignKey('campaigns.campaign_id'),nullable=False)
    user_id=db.Column(UUID(as_uuid=True),db.ForeignKey('users.user_id'),nullable=False)
    comment=db.Column(db.Text,nullable=True)
    user = db.relationship('Users', backref=db.backref('campaigns_comments', lazy=True))
    campaign = db.relationship('Campaigns', backref=db.backref('campaigns_comments', lazy=True))
    is_liked=db.Column(db.Boolean,default=False)
    is_deleted=db.Column(db.Boolean,default=False)
    created_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc),nullable=False)
    updated_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc),onupdate=lambda:datetime.now(timezone.utc),nullable=False)
