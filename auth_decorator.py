from functools import wraps
from flask import jsonify
from flask_dance.contrib.github import github


def check_user_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if github.authorized:
            return f(*args, **kwargs)
        else:
            # If not authorized, return an error response
            return jsonify({'error': 'Unauthorized'}), 401

    return decorated_function
