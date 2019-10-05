from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    body = Column(String())
    posted_at = Column(DateTime, index=True, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User')
    writer_feed_id = Column(Integer, ForeignKey('writer_feeds.id'))
    writer_feed = relationship('WriterFeed')
    hat_id = Column(Integer, ForeignKey('hats.id'))
    hat = relationship('Hat')
    attachments = relationship('Attachment', backref='post')

    def __repr__(self):
        return '<Post {} by {}>'.format(self.id, self.author.username)
