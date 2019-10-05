from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from datetime import datetime
from database import Base

class Attachment(Base):
    __tablename__ = 'attachments'
    id = Column(Integer, primary_key=True)
    attach_type = Column(String)
    url = Column(String())
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Attachment {}>'.format(self.id)
