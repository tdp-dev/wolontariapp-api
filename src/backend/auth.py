from typing import Optional, Annotated
import hashlib
import hmac
import secrets

from beanie import PydanticObjectId
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import BeanieUserDatabase, ObjectIDIDMixin
from fastapi_permissions import configure_permissions, Everyone

from backend.models.user import User, get_user_db
from backend.settings import get_settings


settings = get_settings()


class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.SECRET_KEY, lifetime_seconds=settings.JWT_LIFETIME
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, PydanticObjectId](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)


def get_active_user_principals(
    user: Annotated[User, Depends(current_active_user)]
) -> list[str]:
    permissions = [Everyone]
    if user is not None:
        permissions.append("role:user")
        permissions.append(f"user:{str(user.id)}")
    if user.is_superuser:
        permissions.append(f"role:admin")
    return permissions


Permission = configure_permissions(get_active_user_principals)


def generate_random_token() -> str:
    """Generates random refresh token
    Does not contain expiration date as payload, because expiration date is stored inside SQL database.

    :return: random token
    """
    random_bytes = secrets.token_bytes(64)
    signature = hmac.new(
        settings.SECRET_KEY.encode(),
        random_bytes,
        hashlib.sha256,
    ).hexdigest()
    return signature
