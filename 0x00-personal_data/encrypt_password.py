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

