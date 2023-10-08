from typing import Annotated

from fastapi import APIRouter, Depends

from backend.schemas.notifications import NotificationSchema
from backend.repositories.notification import get_all_notifications, remove_all_notification
from backend.auth import current_active_user
from backend.models import User


router = APIRouter(
    prefix="/notifications",
    tags=["notifications"]
)


@router.get("", response_model=list[NotificationSchema])
async def get_notifications(user: Annotated[User, Depends(current_active_user)]):
    notifications = await get_all_notifications(user)
    await remove_all_notification(user)
    return notifications
