from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from models import User
from database import Base
from uuid import uuid4
from datetime import datetime

class Invite(Base):
    __tablename__ = 'invites'
    invite_code = Column(String(32), primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    redeemed_at = Column(DateTime)
    redeemer_id = Column(Integer, ForeignKey('users.id'))

    def generate_code(self):
        self.invite_code = uuid4().hex

    def redeem(self, user):
        self.redeemed_at = datetime.utcnow()
        self.redeemer_id = user.id

    def __repr__(self):
        return '<Invite {}>'.format(self.invite_code)

def validate_username(username=''):
    username = username.lower()
    if len(username) < 2:
        return False
    u = User.query.filter_by(username=username).first()
    h = Hat.query.filter_by(username=username).first()
    if u is not None or h is not None:
        return False
    return True


def validate_invite_code(invite_code):
    # chicken and egg
    if invite_code == 'superuser':
        if User.query.filter_by(permissions=Permission.Admin).count() > 0:
            return False
        return True
    invite = Invite.query.filter_by(invite_code=invite_code).first()
    print(invite)
    if invite is None:
        return False
    if invite.redeemed_at is not None:
        return False
    return True
