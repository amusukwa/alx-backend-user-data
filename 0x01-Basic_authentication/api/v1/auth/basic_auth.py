#!/usr/bin/env python3
""" Module for base64 decoding"""
import base64
from models.user import User
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ Function for extracting base64 """
        if (authorization_header is None or not isinstance(authorization_header, str) or
                not authorization_header.startswith("Basic ")):
            return None
        else:
            return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """ Decode_base64 function"""
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_bytes.decode('utf-8')
            return decoded_str
        except base64.binascii.Error:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """ Gets user_credentials """
        if (decoded_base64_authorization_header is None or
                not isinstance(decoded_base64_authorization_header, str)):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user_email, user_password = decoded_base64_authorization_header.split(':', 1)
        return user_email, user_password

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> User:
        """ Gets user_object from credentials"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({"email": user_email})
        if not users:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
