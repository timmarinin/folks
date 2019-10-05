from flask import g, jsonify

from models import Hat, User
from api import bp
from api.auth import token_auth
from schema import hats_schema, invites_schema, user_schema


@bp.route('/me')
@token_auth.login_required
def me():
    u = g.current_user
    return jsonify({
        'user': user_schema.dump(u)
    })


@bp.route('/me/hats')
@token_auth.login_required
def my_hats():
    u = g.current_user
    return jsonify(hats=hats_schema.dump(u.hats))


@bp.route('/me/invites')
@token_auth.login_required
def my_invites():
    u = g.current_user
    return jsonify(invites=invites_schema.dump(u.invites))
