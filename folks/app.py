import click
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from config import Config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)


# lower than app = due to circular dependencies
from api import bp as api_bp
from api.errors import error_response as api_err
from database import db_session

app.register_blueprint(api_bp, url_prefix='/api/v2')


@app.cli.command('createdevadmin')
@click.argument('name')
def creatdeveadmin(name):
    from models.user import create_user
    from schema import registration_schema
    registration = registration_schema.load({
        'username': name,
        'password': 'qwerty',
        'invite': 'superuser'
    })
    u = create_user(registration)
    db_session.add(u)
    db_session.commit()

@app.cli.command('reset_password')
@click.argument('username')
@click.argument('password')
def reset_password(username, password):
    from models.user import User
    u = User.query.filter_by(username=username).first()
    u.set_password(password)
    db_session.add(u)
    db_session.delete(u.token)
    db_session.commit()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.errorhandler(404)
def page_not_found(_error):
    return api_err(404)


@app.errorhandler(500)
def internal_error(error):
    db_session.rollback()  # pylint: disable=no-member
    return api_err(500)


@app.route('/__version__')
def version():
    return jsonify(version=2)
