from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def bad_request(msg=None):
    return error_response(400, msg)


def unauthorized(msg=None):
    return error_response(401, msg)


def not_found(msg=None):
    return error_response(404, msg)


def error_response(code, msg=None):
    payload = {
        'error': HTTP_STATUS_CODES.get(code, 'Unknown Error')
    }
    if msg:
        payload['message'] = msg
    response = jsonify(payload)
    response.status_code = code
    return response
