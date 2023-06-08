#!/usr/bin/env python3
"""Auth module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ Hash password
    """
    convert = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(convert, salt)

    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ Initialized
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Register a user
        """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                raise ValueError("User {} already exists".format(user.email))
        except NoResultFound:
            decode_password = _hash_password(password).decode()
            new_user = self._db.add_user(email, decode_password)
            return new_user