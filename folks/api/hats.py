import logging

logger = logging.getLogger(__name__)

from flask import g, jsonify, request

from database import db_session
from models import Hat, Post, User, Permission, WriterFeed, ReaderFeed
from api import bp
from api.auth import token_auth
from api.errors import bad_request, not_found, unauthorized
from schema import hat_schema, hats_schema, posts_schema


@bp.route('/hats')
@token_auth.login_required
def hats():
    all_hats = Hat.query.order_by(Hat.created_at.asc()).all()
    return jsonify(hats=hats_schema.dump(all_hats))


@bp.route('/hats/<username>')
@token_auth.login_required
def hat_detail(username):
    h = Hat.query.filter_by(username=username).first()
    p = Post.query.filter_by(hat_id=h.id).order_by(Post.posted_at.desc()).all()
    return jsonify(hat=hat_schema.dump(h), posts=posts_schema.dump(p))


@bp.route('/hats/<username>', methods=['POST'])
@token_auth.login_required
def edit_hat(username):
    hat = Hat.query.filter_by(username=username).first()
    if hat is None:
        return not_found()
    if g.current_user not in hat.users:
        logger.info('{} попытался отредактировать {}, но не входит в список носителей шляпы'.format(
            g.current_user, hat))
        return unauthorized()

    try:
        hat.display_name = request.json['display_name']
        if request.json.get('add_user', '') is not '':
            u = User.query.filter_by(username=request.json['add_user']).first()
            if u is not None:
                hat.users.append(user)
        hat.about_me = request.json['about_me']
        db_session.add(hat)
        db_session.commit()
        logger.info('{u} обновил шляпу {h}: {d}, {a}, {us}'.format(u=g.current_user,
                                                                   d=hat.display_name,
                                                                   a=hat.about_me,
                                                                   us=hat.users,
                                                                   h=hat))
    except Exception as exc:
        logging.warn('Не получилось отредактировать шляпу {}: {}'.format(hat, exc))
        return bad_request()
    return jsonify(hat=hat_schema.dump(hat))


@bp.route('/hats/<username>/delete', methods=['POST'])
@token_auth.login_required
def delete_hat(username):
    hat = Hat.query.filter_by(username=username).first()
    if hat is None:
        return not_found()
    if not g.current_user.can(Permission.Admin) and not hat.is_wearable_by(g.current_user):
        return unauthorized()
    db_session.delete(hat)
    db_session.commit()
    return jsonify(hat=hat_schema.dump(hat))  # FIXME: test?


@bp.route('/hats', methods=['POST'])
@token_auth.login_required
def create_hat():
    if not g.current_user.can(Permission.CreateHats):
        return unauthorized()

    h = hat_schema.load(request.json)
    users = [g.current_user]

    writer_feed = WriterFeed()
    hat = Hat(username=h['username'],
              users=users,
              writer_feed=writer_feed,
              display_name=h['display_name'],
              about_me=h['about_me'])
    g.current_user.reader_feed.writer_feeds.append(writer_feed)
    db_session.add(hat)
    db_session.commit()
    
    logger.info('{} создал шляпу {}'.format(g.current_user, hat))
    return jsonify(hat=hat_schema.dump(hat))
