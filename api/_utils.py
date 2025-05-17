from functools import wraps
from typing import Type, Callable

from flask import make_response, jsonify

from data import __db_session as db_session


def check_exists(model: Type) -> Callable:
    def check_exists_decorator(function: Callable):
        @wraps(function)
        def wrapper(**kwargs):
            db_sess = db_session.create_session()
            obj = db_sess.get(model, list(kwargs.values())[0])
            if obj is None:
                return make_response(jsonify({'error': 'Not found'}), 404)
            return function(obj)

        return wrapper

    return check_exists_decorator
