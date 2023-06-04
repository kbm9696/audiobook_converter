import base64
from functools import wraps
from flask import request, jsonify
from dba.userdba import UserDba


def validate_user_credentials(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if auth:
            # Decode the base64-encoded credentials
            encoded_credentials = auth.split(' ')[-1]
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')

            # Split the credentials into username and password
            username, password = decoded_credentials.split(':')

        if not validate_credentials(username, password):
            # Return unauthorized response if credentials are invalid
            resp = {'message': 'Invalid credentials'}
            resp = jsonify(resp)
            resp.status = 401
            return resp

        # Call the API endpoint if credentials are valid
        return func(*args, **kwargs)

    return wrapper


def validate_credentials(user_id, password):
    user_dba = UserDba()
    user_data = user_dba.get_by_userid(user_id)
    if not bool(user_data):
        return False
    else:
        if password == user_data['password']:
            return True
        else:
            return False
