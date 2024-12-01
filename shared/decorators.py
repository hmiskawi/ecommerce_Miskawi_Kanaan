from functools import wraps
from flask import session, jsonify, request
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def login_required(f):
    """
    Decorator to ensure that the user is logged in before accessing the endpoint.

    :param f: The function to wrap.
    :type f: function
    :return: The wrapped function or an unauthorized response.
    :rtype: function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            logger.warning("Unauthorized access attempt detected.")
            return jsonify({"message": "Unauthorized! Please log in."}), 401
        logger.info(f"User {session.get('user_id')} accessed {request.path}.")
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Decorator to ensure that the user has admin privileges before accessing the endpoint.

    :param f: The function to wrap.
    :type f: function
    :return: The wrapped function or an unauthorized/forbidden response.
    :rtype: function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            logger.warning("Unauthorized admin access attempt detected.")
            return jsonify({"message": "Unauthorized! Please log in."}), 401
        if session.get('role') != 'admin':
            logger.warning(f"User {session.get('user_id')} attempted to access {request.path} without admin privileges.")
            return jsonify({"message": "Forbidden! Admin access only."}), 403
        logger.info(f"Admin user {session.get('user_id')} accessed {request.path}.")
        return f(*args, **kwargs)
    return decorated_function
