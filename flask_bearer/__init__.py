'''flask-bearer

This module provides a class that can be used to make Flask routes require
bearer authentication tokens.

'''

# pylint: disable=R0903

from functools import wraps
from flask import abort, request

class BearerToken:
    '''Class used to make Flask routes require bearer authentication tokens.'''

    def __init__(self, token: str, unauthorized=lambda: abort(401)):
        self._token = token
        self._unauthorized = unauthorized

    def required(self, function):
        '''Decorator function of a Flask route that makes it require a bearer
        authentication token.

        The function only succeeds if the request header contains the
        Authorization field and if the value of the field is equal to
        "Bearer <token>".

        Otherwise, the function will abort.
        '''
        @wraps(function)
        def decorated_function(*args, **kwargs):
            authorization = request.headers.get('Authorization', '')
            if authorization != f'Bearer {self._token}':
                return self._unauthorized()
            return function(*args, **kwargs)
        return decorated_function
