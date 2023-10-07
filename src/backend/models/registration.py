from enum import Enum
from datetime import datetime

from pydantic import Field

from beanie import Document, Link

from backend.models import Event, User


class RegistrationStatus(Enum):
    REGISTERED = "REGISTERED"
    ACCEPTED = "ACCEPTED"
    REPORT = "REPORT"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"


class Registration(Document):
    event: Link[Event]
    user: Link[User]
    date_created: datetime = Field(default_factory=datetime.now)
    status: RegistrationStatus = Field(default=RegistrationStatus.REGISTERED)
