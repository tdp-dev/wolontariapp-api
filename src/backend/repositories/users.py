from beanie.odm.operators.update.general import Set

from backend.models import User


async def fetch_user(user_id: str) -> User:
    return await User.get(user_id)


async def fetch_many_user(page: int = 0, per_page: int = 10) -> list[User]:
    return await User.find({}).skip(page * per_page).limit(per_page).to_list()


async def update_user(user: User, **user_data):
    await user.update(Set(user_data))


async def delete_user(user: User):
    await user.delete()
