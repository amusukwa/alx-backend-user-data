#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
if 'AUTH_TYPE' in os.environ:
    auth_type = os.environ['AUTH_TYPE']
    if auth_type == 'auth':
        from api.v1.auth.auth import Auth
        auth = Auth()

@app.before_request
def before_request():
    if auth is None:
        return
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
    if request.path in excluded_paths:
        return
    if not auth.require_auth(request.path, excluded_paths):
        abort(401)
    if auth.authorization_header(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized_error(error):
    response = jsonify({"error": "Unauthorized"})
    response.status_code = 401
    return response

@app.errorhandler(403)
def forbidden_error(error):
    response = jsonify({"error": "Forbidden"})
    response.status_code = 403
    return response


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
