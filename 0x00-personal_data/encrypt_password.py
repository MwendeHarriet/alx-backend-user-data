#!/usr/bin/env python3
"""
Encrypting passwords
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a salted, hashed password, which is a byte string."""
    passwd_bytes = password.encode()
    salt = bcrypt.gensalt()
    hashed_passwd = bcrypt.hashpw(passwd_bytes, salt)
    return hashed_passwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validate that the provided password matches the hashed password."""
    result = bcrypt.checkpw(password.encode(), hashed_password)
    return result
