from utils.initdb import db
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime,date,timezone
class NewsLetter(db.Model):
    __tablename__='newsletter'
    news_letter_id=db.Column(UUID(as_uuid=True),primary_key=True)
    name=db.Column(db.String(50),nullable=False,)
    email=db.Column(db.String(50),nullable=False,unique=True)
    subject=db.Column(db.String(50),nullable=False)
    content=db.Column(db.String,nullable=False)
    created_at=db.Column(db.DateTime,default=lambda:datetime.now(timezone.utc))