from flask import Blueprint, url_for, jsonify, abort

bp = Blueprint('api', __name__)

from . import errors, auth, feed, hats, settings, users, me
from models import Flag
@bp.route('/flags/<name>')
def flag(name):
    flag = Flag.query.filter_by(name=name).first()
    if flag is None:
        abort(404)
    return jsonify(flag=dict(name=name, value=flag.value))

@bp.route('/')
@auth.token_auth.login_required
def index():
    return jsonify(_links={
        'hats': url_for('.hats')
    })
