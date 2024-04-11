#!/usr/bin/env python3
"""
Module for hashing password
"""

import bcrypt

def hash_password(password: str) -> bytes:
    # Generate a salt for the password
    salt = bcrypt.gensalt()
    # Hash the password using the generated salt
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

def is_valid(hashed_password: bytes, password: str) -> bool:
    # Use bcrypt's checkpw function to verify if the password matches the hashed password
    return bcrypt.checkpw(password.encode(), hashed_password)

