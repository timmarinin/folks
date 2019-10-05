from sqlalchemy import Table, Integer, ForeignKey, DateTime, Column, String, and_
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base, db_session
import logging
logger = logging.getLogger(__name__)
from werkzeug.security import generate_password_hash, check_password_hash
from models import AccessToken, Permission

users_hats = Table(
    'users_hats', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('hat_id', Integer, ForeignKey('hats.id'))
)


users_reader_feeds = Table(
    'users_readers_feeds', Base.metadata,
    Column('reader_feed_id', Integer, ForeignKey('reader_feeds.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)


class User(Base):
    """
    Folks user
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True, unique=True)
    password = Column(String())
    created_at = Column(DateTime, index=True, default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    registered_at = Column(DateTime, index=True, default=datetime.utcnow)
    permissions = Column(Integer)
    hats = relationship('Hat', secondary=users_hats, passive_deletes=True)

    invites = relationship('Invite', backref="invite_owner",
                           foreign_keys='Invite.owner_id',
                           cascade="all, delete-orphan",
                           passive_deletes=True, single_parent=True)
    invite = relationship('Invite', backref="redeemer",
                          foreign_keys='Invite.redeemer_id',
                          single_parent=True)
    token_id = Column(Integer, ForeignKey('access_tokens.id'))
    token = relationship('AccessToken')
    reader_feed_id = Column(Integer, ForeignKey('reader_feeds.id'))
    reader_feed = relationship('ReaderFeed')
    writer_feed_id = Column(Integer(), ForeignKey('writer_feeds.id'))
    writer_feed = relationship('WriterFeed')

    def get_token(self):
        if self.token is not None:
            return self.token
        else:
            token = AccessToken()
            token.expire_in_2_weeks()
            token.generate_token()
            self.token = token
            return token

    def check_token(token):
        tok = AccessToken.query.filter_by(token=token).first()
        logger.info('found token %s', tok)
        if tok is not None and tok.not_expired():
            return tok.user[0]
        return None

    def can(self, ask):
        if self.permissions is None:
            self.permissions = Permission.User
        return Permission(self.permissions).can(ask)

    def can_have_more_invites(self):
        from models import Invite
        unredeemed_invites = db_session.query(Invite).filter(and_(
            Invite.owner_id == self.id, Invite.redeemed_at.is_(None)))
        return unredeemed_invites.count() == 0

    def __repr__(self):
        return '<User {}>'.format(self.username)


def create_user(registration):
    from models import ReaderFeed, WriterFeed, AccessToken, Hat, Invite, Permission
    from database import db_session
    username = registration['username']

    writer_feed = WriterFeed(description='primary writer feed')
    reader_feed = ReaderFeed(
        description='primary reader feed', writer_feeds=[writer_feed])
    user = User(username=username, writer_feed=writer_feed,
                reader_feed=reader_feed)
    user.set_password(registration['password'])
    db_session.add(user)  # pylint: disable=no-member
    hat = Hat(display_name=username,
              username=username, writer_feed=writer_feed)
    hat.users = [user]
    if registration['invite'] == 'superuser':
        user.permissions = Permission.Admin
    else:
        user.permissions = Permission.User
    invite = Invite.query.filter_by(
        invite_code=registration['invite']).first()
    db_session.add(hat)
    if invite is not None:
        invite.redeem(user)
        db_session.add(invite)
    else:
        logger.info('Creating user {} with no invite'.format(username))
    db_session.commit()
    return user
