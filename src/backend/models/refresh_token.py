from datetime import datetime

from beanie import Document, Link

from backend.models import User


class RefreshToken(Document):
    user: Link[User]
    date_to: datetime
    date_from: datetime
    key: str

    @property
    def is_active(self) -> bool:
        return self.date_to > datetime.now()
