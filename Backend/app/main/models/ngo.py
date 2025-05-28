from datetime import datetime,timezone
from sqlalchemy.dialects.postgresql import UUID
from utils.initdb import db
from utils.enums import Status
import uuid

class NGO(db.Model):
    __tablename__='ngos'
    ngo_id=db.Column(UUID(as_uuid=True),primary_key=True,nullable=False,default=uuid.uuid4)
    ngo_name=db.Column(db.String(150),nullable=False,unique=True)
    ngo_mission=db.Column(db.String(100),nullable=True)
    ngo_status=db.Column(db.Enum(Status),nullable=False,default=Status.pending)
    ngo_location=db.Column(db.String(100),nullable=False)
    ngo_blacklisted=db.Column(db.Boolean,default=False)
    is_verified=db.Column(db.Boolean,default=False)
    user_id=db.Column(UUID(as_uuid=True),db.ForeignKey('users.user_id'),nullable=False,unique=True)
    user=db.relationship('Users',backref=db.backref('ngos',uselist=True))
    is_deleted=db.Column(db.Boolean,default=False)
    created_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc))
    updated_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc),onupdate=lambda:datetime.now(timezone.utc))


