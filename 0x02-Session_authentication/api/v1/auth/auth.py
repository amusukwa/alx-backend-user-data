#!/usr/bin/env python3
""" class module for Authorization"""
from flask import request
from typing import List, TypeVar


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ function for getting authorization"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        path = path.rstrip('/')
        for excluded_path in excluded_paths:
            excluded_path = excluded_path.rstrip('/')
            if path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ function for getting auth header"""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')


    def current_user(self, request=None) -> TypeVar('User'):
        return None

    def session_cookie(self, request: Request = None) -> str:
        """ returns session cookie"""
        if request is None:
            return None
        session_name = os.environ.get('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
