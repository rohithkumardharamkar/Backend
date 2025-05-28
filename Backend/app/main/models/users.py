from datetime import datetime,timezone
from sqlalchemy.dialects.postgresql import UUID
from utils.initdb import db
from utils.enums import Gender,Role
import uuid

class Users(db.Model):
    __tablename__='users'
    user_id=db.Column(UUID(as_uuid=True),primary_key=True,default=lambda:uuid.uuid4())
    user_name=db.Column(db.String(100),nullable=False)
    user_email=db.Column(db.String(150),nullable=False,unique=True,index=True)
    user_mobile=db.Column(db.String(15),nullable=True,unique=True,index=True)
    user_password=db.Column(db.String(100),nullable=True)
    user_gender=db.Column(db.Enum(Gender),nullable=True)
    user_role=db.Column(db.Enum(Role),nullable=True,default=Role.user)
    is_deleted=db.Column(db.Boolean,default=False)
    created_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc))
    updated_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc),onupdate=lambda:datetime.now(timezone.utc))