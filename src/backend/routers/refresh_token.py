from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Body, HTTPException

from backend.settings import get_settings, Settings
from backend.schemas.refresh_token import Token, ValidateRefreshToken
from backend.repositories.refresh_tokens import (
    get_active_refresh_token,
    create_refresh_token,
    deactivate_refresh_token,
)
from backend.auth import (
    current_active_user,
    generate_random_token,
    auth_backend,
    get_jwt_strategy,
)
from backend.models import User


router = APIRouter(prefix="/refresh", tags=["refresh"])


@router.post("", response_model=Token)
async def fetch_new_refresh_token(
    user: Annotated[User, Depends(current_active_user)],
    settings: Annotated[Settings, Depends(get_settings)],
):
    random_token = generate_random_token()
    refresh_token = await create_refresh_token(
        user=user,
        date_to=datetime.now() + timedelta(days=settings.REFRESH_TOKEN_LIFETIME),
        date_from=datetime.now(),
        key=str(random_token),
    )
    return Token(token_type="refresh", access_token=refresh_token.key).model_dump()


@router.post("/login")
async def login_with_refresh_token(
    refresh_token: Annotated[ValidateRefreshToken, Body(...)]
):
    refresh_token = await get_active_refresh_token(key=refresh_token.key)
    if refresh_token is not None:
        return await auth_backend.login(
            strategy=get_jwt_strategy(), user=refresh_token.user
        )
    raise HTTPException(status_code=401, detail="Invalid refresh token")


@router.post("/logout", status_code=204)
async def logout(user: Annotated[User, Depends(current_active_user)]):
    await deactivate_refresh_token(user)
