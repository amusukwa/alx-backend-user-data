#!/usr/bin/env python3
"""auth.py
"""

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Hashes the input password string using bcrypt.hashpw
        """
        # Implement _hash_password method here (as defined in the previous task)

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user with the provided email and password
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

# Usage example
if __name__ == "__main__":
    email = 'me@me.com'
    password = 'mySecuredPwd'

    auth = Auth()

    try:
        user = auth.register_user(email, password)
        print("Successfully created a new user!")
    except ValueError as err:
        print("Could not create a new user: {}".format(err))

    try:
        user = auth.register_user(email, password)
        print("Successfully created a new user!")
    except ValueError as err:
        print("Could not create a new user: {}".format(err))

