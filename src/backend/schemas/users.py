from typing import Optional
from datetime import datetime

from beanie import PydanticObjectId
from fastapi_users import schemas
from pydantic import Field, AliasChoices
from fastapi_users import models


class UserRead(schemas.BaseUser[PydanticObjectId]):
    id: Optional[str | PydanticObjectId] = Field(
        validation_alias=AliasChoices("id", "_id")
    )
    first_name: str
    last_name: str
    age: int
    date_created: datetime


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    age: int


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str
    last_name: str
    age: int
