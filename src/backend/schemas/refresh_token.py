from datetime import datetime

from pydantic import BaseModel, Field


class ValidateRefreshToken(BaseModel):
    key: str


class Token(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")
