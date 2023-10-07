from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi_cache.decorator import cache
from beanie.odm.operators.update.general import Set

from backend.schemas.users import UserRead
from backend.models import User
from backend.repositories.users import (
    fetch_many_user,
)
from backend.auth import current_active_user
from backend.settings import get_settings, Settings
from backend.azure_blob_storage import upload_blob


router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserRead])
@cache(expire=60)
async def get_users(page: int = 0, per_page: int = 10):
    return await fetch_many_user(page, min(per_page, 10))


@router.put("/me/profile-image", response_model=UserRead)
async def update_profile_image(
        user: Annotated[User, Depends(current_active_user)],
        settings: Annotated[Settings, Depends(get_settings)],
        image: Annotated[UploadFile, File(description="New user profile image")],
):
    upload_blob(settings, "profile-images", str(user.id), await image.read())
    await user.update(Set({"profile_img": str(user.id)}))
    return user
