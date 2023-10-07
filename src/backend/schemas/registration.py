from typing import Optional
from datetime import datetime

from pydantic import BaseModel
from beanie import PydanticObjectId
from pydantic import Field, AliasChoices

from backend.models.registration import RegistrationStatus
from backend.schemas.events import EventSchema
from backend.schemas.users import UserRead


class RegistrationSchema(BaseModel):
    id: Optional[str | PydanticObjectId] = Field(
        validation_alias=AliasChoices("id", "_id")
    )
    user: UserRead
    date_created: datetime
    status: RegistrationStatus


class RegistrationStatusChangeSchema(BaseModel):
    status: RegistrationStatus
