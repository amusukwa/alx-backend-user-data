#!/usr/bin/env python3
"""
Route module for the API

This module defines the routes and handlers for the API endpoints.
based on the specified authentication type. Error handlers are also defined.
"""

from os import getenv
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from api.v1.auth.session_auth import SessionAuth
import os
import bcrypt

app = Flask(__name__)
app.register_blueprint(app_views)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Determine authentication type based on environment variable
auth = None
auth_type = getenv('AUTH_TYPE')
if auth_type == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif auth_type == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth_type == 'Auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
else:
    raise ValueError(f"Invalid value for AUTH_TYPE: {auth_type}")


@app.before_request
def before_request():
    """Before request handler

    This function is executed before each request to the API. It performs
    based on the authentication type and the requested endpoint.

    If authentication fails or the user is not authorized,the HTTP error.
    """
    if auth is None:
        return

    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/', '/api/v1/auth_session/login/']
    if request.path in excluded_paths:
        return

    if not auth.require_auth(request.path, excluded_paths):
        abort(401)

    if auth.authorization_header(request) is None:
        abort(401)

    if auth.current_user(request) is None:
        abort(403)

    request.current_user = auth.current_user(request)

    if auth.authorization_header(request) is None and auth.session_cookie(request) is None:
        abort(401)


@app.errorhandler(404)
def not_found(error) -> str:
    """Not found error handler

    This function handles HTTP 404 errors (Not Found) by returning error message.

    Args:
        error: The error object

    Returns:
        JSON response with error message and status code 404
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_error(error):
    """Unauthorized error handler

    This function handles HTTP 401 errors (Unauthorized)

    Args:
        error: The error object

    Returns:
        JSON response with error message and status code 401
    """
    response = jsonify({"error": "Unauthorized"})
    response.status_code = 401
    return response


@app.errorhandler(403)
def forbidden_error(error):
    """Forbidden error handler

    This function handles HTTP 403 errors (Forbidden) by returning

    Args:
        error: The error object

    Returns:
        JSON response with error message and status code 403
    """
    response = jsonify({"error": "Forbidden"})
    response.status_code = 403
    return response


if __name__ == "__main__":
    # Retrieve host and port values from environment variables
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
