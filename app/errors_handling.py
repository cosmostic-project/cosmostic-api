from flask import Blueprint, current_app, request
from pymongo.errors import ServerSelectionTimeoutError

from extensions import jwt
from utils.commons import create_response


handler = Blueprint("errors_handling", __name__)


@handler.app_errorhandler(404)
def page_not_found(_):
    """
    Handles 404 errors.

    Returns:
        Response: The response object with a 404 status code and a message indicating that the endpoint does not exist.
    """
    return create_response(404, "This endpoint does not exist")

@handler.app_errorhandler(405)
def method_not_allowed(_):
    """
    Handles 405 errors.

    Returns:
        Response: The response object with a 405 status code and a message indicating that the method is not allowed.
    """
    return create_response(405, "Method not allowed")

@handler.app_errorhandler(Exception)
def internal_server_error_callback(e):
    """
    A callback function for handling internal server errors.

    Returns:
        Response: The response object with a 500 status code and a message indicating an internal server error.
    """
    current_app.logger.exception(f"{request.remote_addr} - Internal server error : {e}")
    return create_response(500, "Internal Server Error. Contact support")

@handler.app_errorhandler(ServerSelectionTimeoutError)
def server_selection_timeout_callback(e):
    """
    Error handler for ServerSelectionTimeoutError.
    
    Returns:
        Response: The response object with a 500 status code and a message indicating a database timeout error.
    """
    current_app.logger.error(f"Database timeout error : {e}")
    return create_response(500, "Database timeout error. Contact support")


@jwt.unauthorized_loader
def unauthorized_callback(_):
    """
    Callback function for handling unauthorized access.

    Returns:
        Response: The response object with a 401 status code and a message indicating that no token was provided.
    """
    current_app.logger.info(f"{request.remote_addr} - Unauthorized access to {request.path}")
    return create_response(401, "No token provided")

@jwt.invalid_token_loader
def invalid_token_callback(reason):
    """
    A callback function that is called when an invalid JWT token is encountered.

    Returns:
        Response: A response object with a status code of 401 and a message indicating that the token is invalid.
    """
    current_app.logger.info(f"{request.remote_addr} - Invalid token : {reason}")
    return create_response(401, "Invalid token")

@jwt.expired_token_loader
def expired_token_callback(_, payload):
    """
    A callback function that is called when an expired JWT token is encountered.

    Returns:
        Response: A response object with a status code of 401 and a message indicating that the token has expired.
    """
    current_app.logger.info(f"{request.remote_addr} - Expired token for user : {payload.get('sub')}")
    return create_response(401, "Token expired")