#!/usr/bin/env python3
"""auth module
"""

import bcrypt

def _hash_password(password: str) -> bytes:
    """Hashes the input password string using bcrypt.hashpw
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

# Usage example
if __name__ == "__main__":
    print(_hash_password("Hello Holberton"))

