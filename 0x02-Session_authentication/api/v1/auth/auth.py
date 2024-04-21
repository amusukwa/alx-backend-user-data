#!/usr/bin/env python3
"""Class module for Authorization"""

from typing import List, TypeVar
from flask import Request


class Auth:
    """Class Auth for authorization"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Function for checking if authentication is required for a given path.

        Args:
            path (str): The path to check for authentication requirement.
            excluded_paths (List[str]): List of paths that are excluded

        Returns:
            bool: True if authentication is required, False if not.
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        path = path.rstrip('/')
        for excluded_path in excluded_paths:
            excluded_path = excluded_path.rstrip('/')
            if path == excluded_path:
                return False

        return True

    def authorization_header(self, request: Request = None) -> str:
        """
        Function for getting the authorization header from a request.

        Args:
            request (Request, optional): The Flask request object.

        Returns:
            str: The authorization header if present, else None.
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request: Request = None) -> TypeVar('User'):
        """
        Function for getting the current user.

        Args:
            request (Request, optional): The Flask request object.

        Returns:
            User: The current user object.
        """
        return None

    def session_cookie(self, request: Request = None) -> str:
        """
        Function for getting the session cookie from a request.

        Args:
            request (Request, optional): The Flask request object.

        Returns:
            str: The session cookie if present, else None.
        """
        return None
