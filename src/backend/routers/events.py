from typing import Annotated
import json

from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from fastapi_cache.decorator import cache
from beanie.odm.operators.update.general import Set
from pydantic import ValidationError

from backend.schemas.events import EventSchema, CreateEventSchema
from backend.models import Event
from backend.repositories.google_maps import resolve_address, fetch_map_preview
from backend.repositories.events import update_event, insert_event, fetch_event, fetch_many_events
from backend.settings import get_settings, Settings
from backend.azure_blob_storage import upload_blob


router = APIRouter(
    prefix="/events",
    tags=["events"]
)


@router.post("", response_model=EventSchema)
async def create_event(
    event_data: Annotated[str, Form()],
    image: Annotated[UploadFile, File()],
    settings: Annotated[Settings, Depends(get_settings)],
):
    try:
        valid_event = CreateEventSchema(**json.loads(event_data))
    except ValidationError as error_msg:
        return HTTPException(status_code=400, detail=error_msg)
    except json.JSONDecodeError:
        return HTTPException(status_code=400, detail="Invalid JSON schema")
    db_event = await insert_event(**valid_event.model_dump())
    resolved_address = resolve_address(*valid_event.location.coordinates, settings.GOOGLE_API_KEY)
    location_preview = fetch_map_preview(*valid_event.location.coordinates, settings.GOOGLE_API_KEY)
    upload_blob(settings, "event-preview", str(db_event.id), location_preview)
    upload_blob(settings, "event-images", str(db_event.id), await image.read())
    await update_event(db_event, address=resolved_address, preview=str(db_event.id), image=str(db_event.id))
    return await fetch_event(str(db_event.id))


@router.get("", response_model=list[EventSchema])
async def list_events(page: int = 0, per_page: int = 10):
    return await fetch_many_events(page, per_page)


@router.get("/{event_id}", response_model=EventSchema)
async def retrieve_event(event_id: str):
    return await fetch_event(event_id)
