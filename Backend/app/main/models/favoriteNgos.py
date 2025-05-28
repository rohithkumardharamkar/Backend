from datetime import datetime,timezone
from sqlalchemy.dialects.postgresql import UUID
from utils.initdb import db
import uuid
class FavoriteNGO(db.Model):
    __tablename__='favorite_ngo'
    favorite_id=db.Column(UUID(as_uuid=True),primary_key=True,nullable=False,default=uuid.uuid4)
    ngo_id=db.Column(UUID(as_uuid=True),db.ForeignKey('ngos.ngo_id'),nullable=False)
    user_id=db.Column(UUID(as_uuid=True),db.ForeignKey('users.user_id'),nullable=False)
    ngo=db.relationship('NGO',backref=db.backref('favorite_ngo',lazy=True))
    user=db.relationship('Users',backref=db.backref('favorite_ngo'),lazy=True)
    is_deleted=db.Column(db.Boolean,default=False)
    created_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc))
    updated_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc),onupdate=lambda:datetime.now(timezone.utc))