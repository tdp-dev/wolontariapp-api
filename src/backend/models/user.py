from beanie import Document
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase
from fastapi_permissions import Allow


class User(BeanieBaseUser, Document):
    pass

    def __acl__(self):
        return [
            (Allow, f"user:{str(self.id)}", "view"),
            (Allow, "role:admin", "view"),
            (Allow, "role:admin", "update"),
            (Allow, f"user:{str(self.id)}", "delete"),
            (Allow, "role:admin", "delete"),
        ]


async def get_user_db():
    yield BeanieUserDatabase(User)
