#!/usr/bin/env python3
"""app.py - Flask app with a single GET route"""

from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
auth = Auth()

@app.route("/")
def welcome() -> str:
    """Welcome route returning a JSON payload"""
    return jsonify({"message": "Bienvenue"})

@app.route("/register", methods=["POST"])
def register() -> str:
    """Endpoint to register a user"""
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Attempt to register the user
        user = auth.register_user(email, password)
        
        # User successfully registered
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError as err:
        # User already registered
        return jsonify({"message": "email already registered"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
