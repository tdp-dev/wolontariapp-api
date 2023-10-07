from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import field_validator, Field
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase
from fastapi_permissions import Allow


class User(BeanieBaseUser, Document):
    first_name: str
    last_name: str
    profile_img: Optional[str] = None
    age: int
    date_created: datetime = Field(default_factory=datetime.now)

    def __acl__(self):
        return [
            (Allow, f"user:{str(self.id)}", "view"),
            (Allow, "role:admin", "view"),
            (Allow, "role:admin", "update"),
            (Allow, f"user:{str(self.id)}", "delete"),
            (Allow, "role:admin", "delete"),
        ]

    # @field_validator("date_created")
    # def get_date_created(self, value):
    #     return datetime.now()


async def get_user_db():
    yield BeanieUserDatabase(User)
