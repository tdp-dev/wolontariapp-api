from fastapi import FastAPI
from beanie import init_beanie
from redis import asyncio as aioredis
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache

from backend.db import db
from backend.models import User, RefreshToken
from backend.schemas.users import UserCreate, UserRead, UserUpdate
from backend.auth import auth_backend, fastapi_users
from backend.routers import refresh_token, users
from backend.settings import get_settings

SETTINGS = get_settings()

app = FastAPI()
app.include_router(router=users.router)
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
app.include_router(router=refresh_token.router)


@app.on_event("startup")
async def on_startup():
    await init_beanie(
        database=db,
        document_models=[
            User,
            RefreshToken,
        ],
    )
    redis = aioredis.from_url(SETTINGS.REDIS_URI)
    FastAPICache.init(RedisBackend(redis), prefix=SETTINGS.REDIS_PREFIX)
