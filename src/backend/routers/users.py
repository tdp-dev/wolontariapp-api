from fastapi import APIRouter
from fastapi_cache.decorator import cache

from backend.schemas.users import UserRead
from backend.repositories.users import (
    fetch_many_user,
)


router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserRead])
@cache(expire=60)
async def get_users(page: int = 0, per_page: int = 10):
    return await fetch_many_user(page, min(per_page, 10))
