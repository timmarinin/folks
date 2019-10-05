
import base64
import os
import datetime
import logging
logger = logging.getLogger(__name__)
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class AccessToken(Base):
    """
    Random token that maps to user
    """
    __tablename__ = 'access_tokens'
    id = Column(Integer, primary_key=True)
    token = Column(String(256), index=True, unique=True)
    description = Column(String(256))
    user = relationship('User')
    expiration_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


    def not_expired(self):
        return self.expiration_date > datetime.datetime.utcnow()

    def expire_in_2_weeks(self):
        logger.info('Renewed expiration date for token {}'.format(self.id))
        self.expiration_date = datetime.datetime.utcnow() + datetime.timedelta(days=14)

    def generate_token(self):
        self.token = base64.b64encode(os.urandom(32)).decode('utf-8')

    def __repr__(self):
        return '<AccessToken for {}>'.format(self.user)
