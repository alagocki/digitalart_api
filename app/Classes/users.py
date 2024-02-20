from fastapi import Depends
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase

from app.Database.db import get_user_db

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"


class UserManager(UUIDIDMixin, BaseUserManager):
    reset_password_token_secret = SECRET_KEY
    verification_token_secret = SECRET_KEY


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


# cookie_transport = CookieTransport(cookie_httponly=True, cookie_secure=True)
bearer_transport = BearerTransport(tokenUrl="/login")


def get_jwt():
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt", transport=bearer_transport, get_strategy=get_jwt
)


fastapi_users = FastAPIUsers(get_user_manager, [auth_backend])


active_user = fastapi_users.current_user(active=True)
