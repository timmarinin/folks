import logging

from flask import g, jsonify, request
from flask_httpauth import HTTPTokenAuth

from database import db_session
from models import User, AccessToken
from api import bp
from api.errors import bad_request, error_response, unauthorized
from schema import token_schema, user_schema, pass_auth_schema, ValidationError

logger = logging.getLogger(__name__)

token_auth = HTTPTokenAuth()

@bp.route('/token', methods=['GET'])
@token_auth.login_required
def check_token():
    return jsonify(ok=True)

@bp.route('/token', methods=['POST'])
def get_token():
    try:
        p = pass_auth_schema.load(request.json)
    except ValidationError as exc:
        return bad_request()
    u = User.query.filter_by(username=p['username']).first()
    if u is None:
        return unauthorized('Не получилось залогиниться')
    if u.check_password(p['password']):
        token = u.get_token()
        token.expire_in_2_weeks()
        db_session.add(token)
        db_session.add(u)
        db_session.commit()

        return jsonify(token=token_schema.dump(token), username=u.username,user=user_schema.dump(u))
    return unauthorized('Не получилось залогиниться')


@token_auth.verify_token
def verify_token(token):
    if token is not None:
        u = User.check_token(token)
    else:
        u = None
    g.current_user = u
    return g.current_user is not None


@token_auth.error_handler
def token_auth_error():
    return error_response(401, 'Неправильные креденшиалы')
