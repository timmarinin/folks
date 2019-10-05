import datetime

from flask import g, jsonify

from database import db_session
from models import Invite, User
from api import bp
from api.auth import token_auth
from api.errors import bad_request
from schema import invite_schema


@bp.route('/settings/gen_invites', methods=['POST'])
@token_auth.login_required
def gen_invites():
    u = g.current_user

    if u.can_have_more_invites():
        invite = Invite()
        invite.generate_code()
        g.current_user.invites.append(invite)
        db_session.add(invite)
        db_session.commit()
        return jsonify(invite=invite_schema.dump(invite))
    return bad_request('UNREDEEMED')


@bp.route('/settings/profle', methods=['GET', 'POST'])
@token_auth.login_required
def profile():
    pass
