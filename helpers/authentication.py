from http import HTTPStatus
from flask import session


def require_login(f):
    def wrapper(*args, **kwargs):
        if session.get("user") is None:
            return {"message": "User not logged in"}, HTTPStatus.UNAUTHORIZED
        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__

    return wrapper
