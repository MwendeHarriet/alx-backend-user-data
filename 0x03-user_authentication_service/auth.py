#!/usr/bin/env python3
"""Module define a _hash_password method that takes in a password
    string arguments and returns bytes."""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Union


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """Init"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Take mandatory email and password string arguments
        and return a User object
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass
        hashed_pwd = _hash_password(password)
        user_obj = self._db.add_user(email, hashed_pwd)
        return user_obj

    def valid_login(self, email: str, password: str) -> bool:
        """Credentials validation"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                password_bytes = password.encode('utf-8')
            return bcrypt.checkpw(password_bytes, user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """
        Returns the session ID as a string
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            return session_id
        except NoResultFound:
            pass

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Find user by session ID"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy session"""
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generate reset password token"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()
        new_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=new_password,
                             reset_token=None)


def _hash_password(password: str) -> bytes:
    """
    Takes in a password string arguments and returns bytes
    """
    decoded_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    result = bcrypt.hashpw(decoded_bytes, salt)
    return result


def _generate_uuid() -> str:
    """
    Return a string representation of a new UUID
    """
    return str(uuid.uuid4())
