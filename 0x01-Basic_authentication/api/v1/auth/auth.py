#!/usr/bin/env python3
""" class module for Authorization"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Class for managing authorization"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ function for getting authorization"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            else:
                if path == excluded_path.rstrip('/'):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """ function for getting auth header"""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ function for getting current user"""
        return None
