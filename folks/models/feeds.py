from sqlalchemy import Table, Integer, ForeignKey, String, DateTime, Column
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base

subscriptions = Table(
    'subscriptions', Base.metadata,
    Column('writer_feed_id', Integer, ForeignKey('writer_feeds.id')),
    Column('reader_feed_id', Integer, ForeignKey('reader_feeds.id'))
)

class WriterFeed(Base):
    __tablename__ = 'writer_feeds'
    id = Column(Integer, primary_key=True)
    feed_type = Column(String())
    description = Column(String())
    posts = relationship('Post', back_populates='writer_feed',
                         cascade='all, delete-orphan',
                         passive_deletes=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<WriterFeed {}>'.format(self.id)

class ReaderFeed(Base):
    __tablename__ = 'reader_feeds'
    id = Column(Integer, primary_key=True)
    reader_feed_type = Column(String())
    description = Column(String())
    writer_feeds = relationship('WriterFeed', secondary=subscriptions)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<ReaderFeed {}>'.format(self.id)
