#!/usr/bin/env python3
"""Auth class"""

from flask import request
from typing import List, TypeVar
import os


class Auth:
    """Contains public methods in Auth"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Public method: require_auth"""
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        if path in excluded_paths:
            return False
        for excluded_path in excluded_paths:
            if excluded_path.endswith("*") and\
             path.startswith(excluded_path[:-1].rstrip('/')):
                return False
            elif path.rstrip('/') == excluded_path.rstrip('/'):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Public method: authorization_header"""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Public method: current_user"""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
