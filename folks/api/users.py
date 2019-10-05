import logging
logger = logging.getLogger(__name__)

from flask import g, jsonify, request
from werkzeug.urls import url_parse

from database import db_session
from models import Hat, Invite, Permission, User, WriterFeed, ReaderFeed
from models.user import create_user
from api import bp
from api.errors import bad_request
from api.auth import token_auth
from schema import token_schema, registration_schema, user_schema, ValidationError, hats_schema


@bp.route('/users', methods=['POST'])
def register():
    try:
        registration = registration_schema.load(request.json)
    except ValidationError as exc:
        logger.info('Не получилось зарегистрироваться {}'.format(exc))
        return bad_request('Не хватает полей')
    u = create_user(registration)
    token = u.get_token()
    db_session.add(token)
    db_session.commit()
    return jsonify(user=user_schema.dump(u), token=token_schema.dump(token))


@bp.route('/subscriptions', methods=['POST'])
@token_auth.login_required
def subscribe():
    h = Hat.query.filter_by(username=request.json['username']).first()
    if h is None:
        abort(404)
    feed = h.writer_feed
    g.current_user.reader_feed.writer_feeds.append(feed)
    db_session.add(g.current_user)
    db_session.commit()
    return jsonify(ok=True)

@bp.route('/subscriptions', methods=['GET'])
@token_auth.login_required
def subscriptions():
    u = g.current_user
    subscriptions = [f.id for f in u.reader_feed.writer_feeds]
    writers = db_session.query(Hat).join(WriterFeed).filter(WriterFeed.id.in_(subscriptions)).all()
    print("Writers: {}".format(writers))
    return jsonify(subscriptions=hats_schema.dump(writers))

@bp.route('/subscriptions/<username>', methods=['GET'])
@token_auth.login_required
def is_subscribed(username):
    h = Hat.query.filter_by(username=username).first()
    if h is None:
        abort(404)
    feed = h.writer_feed
    subscribed = feed in g.current_user.reader_feed.writer_feeds
    return jsonify(subscribed=subscribed)

@bp.route('/subscriptions/<username>', methods=['DELETE'])
@token_auth.login_required
def delete_subscription(username):
    u = g.current_user
    delu = Hat.query.filter_by(username=username).first()
    if delu is None:
        return bad_request('Нет такой шляпы')
    u.reader_feed.writer_feeds.remove(delu.writer_feed)
    db_session.add(u)
    db_session.commit()
    return jsonify(ok=True)