from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from models.user import users_hats

class Hat(Base):
    __tablename__ = 'hats'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True, unique=True)
    display_name = Column(String(32))
    about_me = Column(String(256))
    users = relationship('User', secondary=users_hats)
    posts = relationship('Post', backref='author', cascade='all, delete-orphan',
                         passive_deletes=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    writer_feed_id = Column(Integer, ForeignKey('writer_feeds.id'))
    writer_feed = relationship('WriterFeed')
    avatar_url = Column(String())

    def __repr__(self):
        return '<Hat {}>'.format(self.username)

    def is_wearable_by(self, user):
        return user in self.users
