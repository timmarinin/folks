import logging
logger = logging.getLogger(__name__)

from flask import g, jsonify, request, abort

from database import db_session
from models import Post, ReaderFeed, WriterFeed, Hat
from tasks.images import upload_workflow
from tasks.feeds import notify_readers
from api import bp
from api.auth import token_auth
from api.errors import bad_request, unauthorized
from schema import post_schema, new_post_schema, posts_schema


@bp.route('/feed')
@token_auth.login_required
def get_feed():
    feeds = [f.id for f in g.current_user.reader_feed.writer_feeds]
    logger.info('Фиды {}'.format(feeds))
    p = db_session.query(Post).join(WriterFeed).filter(
        WriterFeed.id.in_(feeds)).order_by(Post.posted_at.desc()).limit(30).all()
    return jsonify(posts=posts_schema.dump(p))


@bp.route('/feed', methods=['POST'])
@token_auth.login_required
def create_post():
    p = new_post_schema.load(request.json)
    hat = Hat.query.filter_by(username=request.json['username']).first()
    if hat is None:
        hat = g.current_user.hats[0]
    if not hat.is_wearable_by(g.current_user):
        logger.info('Пользователь {} пытался запостить со шляпой {}'.format(
            g.current_user, hat))
        return unauthorized('Не твоя шляпа')
    if p is not None:
        p.author = hat
        p.user = g.current_user
        p.writer_feed = hat.writer_feed
        db_session.add(p)
        db_session.commit()
        logger.info('Created post {}'.format(p))
        notify_readers.delay(p.writer_feed.id, p.id)
        return jsonify(post=post_schema.dump(p))
    return bad_request('Не тот формат')


@bp.route('/feed/<int:id>', methods=['PATCH'])
@token_auth.login_required
def edit_post(id):
    p = Post.query.filter_by(id=id).first()
    if p is None:
        abort(404)
    if p.user != g.current_user:
        return unauthorized()
    update = post_schema.load(request.json)
    p.body = update['body']
    db_session.add(p)
    db_session.commit()
    return jsonify(post=post_schema.dump(p))


@bp.route('/attachments/image', methods=['POST'])
@token_auth.login_required
def upload_image():
    if request.method != 'POST':
        abort(400)
    if 'file' not in request.files:
        abort(400)
    file = request.files['file']
    if file.filename == '':
        abort(400)
    ext = get_ext(file.filename)
    if file and ext in ALLOWED_EXTENSIONS:
        filename = secure_filename('{}{}'.format(str(uuid4()), ext))
        path = os.path.join(app.config['UPLOAD_TMP_DIR'], filename)
        file.save(path)
        upload = upload_workflow(path).get()
        return jsonify(ok=True, result=upload)
    abort(400)
