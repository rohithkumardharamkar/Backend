from datetime import datetime,timezone
from sqlalchemy.dialects.postgresql import UUID
from utils.initdb import db
import uuid
class Beneficiaries(db.Model):
    __tablename__='beneficiaries'
    beneficiary_id=db.Column(UUID(as_uuid=True),primary_key=True,nullable=False,default=uuid.uuid4)
    ngo_id=db.Column(UUID(as_uuid=True),db.ForeignKey('ngos.ngo_id'),nullable=False)
    beneficiary_name=db.Column(db.String(100),nullable=False)
    beneficiary_address=db.Column(db.String(255),nullable=True)
    ngo=db.relationship('NGO',backref=db.backref('beneficiary',lazy=True))
    is_deleted=db.Column(db.Boolean,default=False)
    created_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc))
    updated_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc),onupdate=lambda:datetime.now(timezone.utc))