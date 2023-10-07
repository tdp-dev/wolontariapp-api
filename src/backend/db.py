import motor.motor_asyncio

from backend.settings import get_settings

settings = get_settings()

client = motor.motor_asyncio.AsyncIOMotorClient(
    settings.MONGO_URI, uuidRepresentation="standard"
)
db = client[settings.MONGO_DB]
