from functools import lru_cache

from pydantic import BaseConfig
from environs import Env


env = Env()


class Settings(BaseConfig):
    MONGO_URI = env("MONGO_URI")
    MONGO_DB = env("MONGO_DB")
    REDIS_URI = env("REDIS_URI")
    REDIS_PREFIX = env("REDIS_PREFIX")
    SECRET_KEY = env("SECRET_KEY")
    JWT_LIFETIME = env.int("JWT_LIFETIME")
    REFRESH_TOKEN_LIFETIME = env.int("REFRESH_TOKEN_LIFETIME")


@lru_cache
def get_settings() -> Settings:
    return Settings()
