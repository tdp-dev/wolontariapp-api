from typing import Optional

from beanie import PydanticObjectId
from fastapi_users import schemas
from pydantic import Field, AliasChoices
from fastapi_users import models


class UserRead(schemas.BaseUser[PydanticObjectId]):
    id: Optional[str | PydanticObjectId] = Field(
        validation_alias=AliasChoices("id", "_id")
    )


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
