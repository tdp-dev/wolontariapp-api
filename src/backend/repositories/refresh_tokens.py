from datetime import datetime

from beanie.odm.operators.update.general import Set

from backend.models import RefreshToken, User


async def create_refresh_token(**refresh_token_data) -> RefreshToken:
    return await RefreshToken(**refresh_token_data).insert()


async def deactivate_refresh_token(user: User):
    await RefreshToken.find(RefreshToken.user.id == user.id).update(
        Set({"date_to": datetime.now()})
    )


async def get_active_refresh_token(key: str) -> RefreshToken | None:
    return await RefreshToken.find_one(
        RefreshToken.key == key, RefreshToken.date_to > datetime.now(), fetch_links=True
    )
