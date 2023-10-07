from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from backend.models.geo import GeoObject
from beanie import PydanticObjectId
from pydantic import Field, AliasChoices


class Day(BaseModel):
    date: datetime
    hours: str


class CreateEventSchema(BaseModel):
    title: str
    description: str
    organization: str
    date: str
    days: list[Day]
    location: GeoObject


class EventSchema(BaseModel):
    id: Optional[str | PydanticObjectId] = Field(
        validation_alias=AliasChoices("id", "_id")
    )
    title: str
    description: str
    organization: str
    date: datetime
    days: list[Day]
    image: Optional[str]
    location: GeoObject
    preview: Optional[str]
    image: Optional[str]
    address: Optional[str]


