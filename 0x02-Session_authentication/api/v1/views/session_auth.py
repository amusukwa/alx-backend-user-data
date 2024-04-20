#!/usr/bin/env python3
"""Module for Session Authentication views"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Endpoint to handle user login"""
    from api.v1.app import auth
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user[0].id)
    user_data = user[0].to_json()

    response = jsonify(user_data)
    response.set_cookie(auth.session_name, session_id)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'])
def logout():
    """Logout route."""
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({})
