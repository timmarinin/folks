from sqlalchemy import Column, Integer, String
from database import Base

class Flag(Base):
    __tablename__ = 'flags'
    name = Column(String(), primary_key=True)
    value = Column(Integer())
