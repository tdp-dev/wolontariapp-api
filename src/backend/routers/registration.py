from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Body

from backend.schemas.registration import RegistrationSchema, RegistrationStatusChangeSchema
from backend.repositories.registration import (
    insert_registration,
    update_registration,
    fetch_one_registration,
    fetch_many_registrations
)
from backend.repositories.notification import create_notification
from backend.repositories.events import fetch_event
from backend.auth import current_active_user
from backend.models import User
from backend.models.registration import RegistrationStatus


router = APIRouter(
    prefix="/events/{event_id}/registrations"
)


@router.post("", response_model=RegistrationSchema)
async def create_registration(event_id: str, user: Annotated[User, Depends(current_active_user)]):
    event = await fetch_event(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event does not exists.")
    return await insert_registration(event=event, user=user)


@router.get("", response_model=list[RegistrationSchema])
async def get_many_registrations(event_id: str, page: int = 0, per_page: int = 10, status: RegistrationStatus | None = None):
    event = await fetch_event(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event does not exists.")
    return await fetch_many_registrations(event, page, per_page, status)


@router.patch("/{registration_id}", response_model=RegistrationSchema)
async def patch_registration(event_id: str, registration_id: str, status: Annotated[RegistrationStatus, Body(...)]):
    registration = await fetch_one_registration(registration_id)
    if registration is None:
        raise HTTPException(status_code=404, detail="Registration does not exists.")
    await update_registration(registration, status=status)
    event = await fetch_event(event_id)
    if status == RegistrationStatus.ACCEPTED:
        await create_notification(user=registration.user, details=f"Twoje zgłoszenie na {event.title} zostało przyjęte")
    elif status == RegistrationStatus.REJECTED:
        await create_notification(user=registration.user, details=f"Twoje zgłoszenie na {event.title} zostało odrzucone")
    return await fetch_one_registration(registration_id)

