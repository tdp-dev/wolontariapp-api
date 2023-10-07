from datetime import datetime, date
from typing import Optional

from beanie import Document
from pydantic import field_validator, Field
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase
from fastapi_permissions import Allow
from pymongo import IndexModel
from pymongo.collation import Collation

from backend.settings import get_settings
from backend.azure_blob_storage import generate_blob_url


settings = get_settings()


class User(BeanieBaseUser, Document):
    first_name: str
    last_name: str
    profile_img: Optional[str] = None
    date_of_born: datetime
    date_created: datetime = Field(default_factory=datetime.now)

    def __acl__(self):
        return [
            (Allow, f"user:{str(self.id)}", "view"),
            (Allow, "role:admin", "view"),
            (Allow, "role:admin", "update"),
            (Allow, f"user:{str(self.id)}", "delete"),
            (Allow, "role:admin", "delete"),
        ]

    @field_validator("profile_img")
    def get_preview_url(cls, value):
        settings = get_settings()
        if value is not None:
            return generate_blob_url(settings, "profile-images", value)


async def get_user_db():
    yield BeanieUserDatabase(User)
