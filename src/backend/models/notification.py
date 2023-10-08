from datetime import datetime

from beanie import Document, Link
from pydantic import Field

from backend.models import User


class Notification(Document):
    user: Link[User]
    details: str
    date: datetime = Field(default_factory=datetime.now)
