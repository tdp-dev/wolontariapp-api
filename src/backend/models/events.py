from typing import Optional
from datetime import datetime

from beanie import Document
from pydantic import BaseModel, field_validator

from backend.models.geo import GeoObject
from backend.settings import get_settings
from backend.azure_blob_storage import generate_blob_url


class Day(BaseModel):
    date: datetime
    hours: str


class Event(Document):
    title: str
    description: str
    organization: str
    date: datetime
    days: list[Day]
    image: Optional[str] = None
    location: GeoObject
    preview: Optional[str] = None
    address: Optional[str] = None

    @field_validator("image")
    def get_images_urls(cls, value):
        settings = get_settings()
        if value is not None:
            return generate_blob_url(settings, "event-images", value)

    @field_validator("preview")
    def get_preview_url(cls, value):
        settings = get_settings()
        if value is not None:
            return generate_blob_url(settings, "event-preview", value)
