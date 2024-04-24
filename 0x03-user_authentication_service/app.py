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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=500)
