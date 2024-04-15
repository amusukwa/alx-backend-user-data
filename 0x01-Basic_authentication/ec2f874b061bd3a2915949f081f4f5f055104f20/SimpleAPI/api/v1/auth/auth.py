from flask import request
from typing import List, TypeVar

class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        path = path.rstrip('/')
        for excluded_path in excluded_paths:
            excluded_path = excluded_path.rstrip('/')
            if path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        return None
