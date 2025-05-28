from utils.initdb import db
from datetime import datetime,timezone

from sqlalchemy.dialects.postgresql import UUID
import uuid
class Blogs(db.Model):
    __tablename__='blogs'
    blog_id=db.Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4())
    ngo_id=db.Column(UUID(as_uuid=True),db.ForeignKey('ngos.ngo_id'),nullable=False)
    blog_description=db.Column(db.Text,nullable=False)
    ngo=db.relationship('NGO',backref=db.backref('blogs',uselist=True))
    is_deleted=db.Column(db.Boolean,default=False)
    created_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc))
    updated_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc),onupdate=lambda:datetime.now(timezone.utc))

