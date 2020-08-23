from functools import wraps
from flask import abort, request

class BearerToken:

    def __init__(self, token, unauthorized = lambda: abort(401)):
        self._token = token
        self._unauthorized = unauthorized

    def required(self, function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            authorization = request.headers.get('Authorization', '')
            if not authorization.startswith('Bearer '):
                return self._unauthorized()
            if authorization[7:] != self._token:
                return self._unauthorized()
            return function(*args, **kwargs)
        return decorated_function
