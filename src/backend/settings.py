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
    AZURE_STORAGE = {
        "ACCOUNT_NAME": env("AZURE_STORAGE_ACCOUNT_NAME"),
        "KEY": env("AZURE_STORAGE_ACCOUNT_KEY"),
        "SAS_LIFETIME": env.int("AZURE_STORAGE_SAS_LIFETIME"),
    }
    GOOGLE_API_KEY = env("GOOGLE_API_KEY")


@lru_cache
def get_settings() -> Settings:
    return Settings()
