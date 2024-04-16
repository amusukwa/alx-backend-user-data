#!/usr/bin/env python3
""" module for base64 decoding"""
import base64


class BasicAuth:
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        if authorization_header is None or not isinstance(authorization_header, str) or not authorization_header.startswith("Basic "):
            return None
        else:
            return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_bytes.decode('utf-8')
            return decoded_str
        except:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        user_email, user_password = decoded_base64_authorization_header.split(':', 1)
        return user_email, user_password
