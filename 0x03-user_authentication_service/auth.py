#!/usr/bin/env python3
"""auth.py
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Hashes the input password string using bcrypt.hashpw."""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user with the provided email and password."""
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if the provided email and password are valid for login."""
        try:
            user = self._db.find_user_by(email=email)
            # Check if the provided password matches the hashed password
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False
