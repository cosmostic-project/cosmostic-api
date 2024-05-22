from flask import current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps

from utils import validator
from utils.commons import create_response


def check_uuid(f):
    """
    Decorator function that checks if the provided UUID is valid.

    Parameters:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function.

    Raises:
        ValueError: If the provided UUID is invalid.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        key, uuid = kwargs.popitem()   # get uuid string from kwargs

        # check if uuid is valid
        try:
            uuid = validator.uuid(uuid)
        except ValueError:
            return create_response(400, "Invalid uuid")

        kwargs[key] = uuid   # replace uuid string with uuid object in kwargs
        return f(*args, **kwargs)
    return decorated


def ensure_uuid_match(f):
    """
    Decorator function that ensures the UUID in the JWT identity matches the UUID provided in the kwargs.

    Parameters:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function.
        Response: A 400 response if the UUIDs don't match.
    """
    @jwt_required()
    @wraps(f)
    def decorated(*args, **kwargs):
        # get jwt identity from jwt
        jwt_identity = get_jwt_identity()
        jwt_identity = validator.uuid(jwt_identity) if isinstance(jwt_identity, str) else jwt_identity

        # get user uuid from kwargs
        user_uuid = kwargs.get('user_uuid')
        user_uuid = validator.uuid(user_uuid) if isinstance(user_uuid, str) else user_uuid

        if jwt_identity != user_uuid:   # if uuids don't match
            return create_response(400, "Unauthorized")
        return f(*args, **kwargs)
    return decorated

def ensure_admin(f):
    """
    Decorator function that ensures the user from jwt identity is an admin.

    Parameters:
        f (function): The function to be decorated.

    Returns:
        function: The decorated function.
        Response: A 400 response if the user is not an admin.
    """
    @jwt_required()
    @wraps(f)
    def decorated(*args, **kwargs):
        # get jwt identity from jwt
        jwt_identity = get_jwt_identity()
        jwt_identity = validator.uuid(jwt_identity) if isinstance(jwt_identity, str) else jwt_identity

        # check if user is admin
        admins = current_app.config.get('ADMINS')
        if not admins or jwt_identity not in admins:
            return create_response(400, "Unauthorized")
        return f(*args, **kwargs)
    return decorated