from typing import Optional
from datetime import datetime

from beanie import PydanticObjectId
from pydantic import Field, AliasChoices, BaseModel


class NotificationSchema(BaseModel):
    id: Optional[str | PydanticObjectId] = Field(
        validation_alias=AliasChoices("id", "_id")
    )
    details: str
    date: datetime
