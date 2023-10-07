from typing import Optional
from datetime import datetime, date

from beanie import PydanticObjectId
from fastapi_users import schemas
from pydantic import Field, AliasChoices, field_validator, model_validator

from backend.repositories.registration import fetch_user_events_count


class UserRead(schemas.BaseUser[PydanticObjectId]):
    id: Optional[str | PydanticObjectId] = Field(
        validation_alias=AliasChoices("id", "_id")
    )
    first_name: str
    last_name: str
    date_of_born: date
    date_created: datetime
    profile_img: Optional[str] = None
    events_count: Optional[int] = None


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    date_of_born: str


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str
    last_name: str
    age: int
