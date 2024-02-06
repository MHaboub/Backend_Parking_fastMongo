from motor.motor_asyncio import AsyncIOMotorClient
from configuration.conf import settings

client = AsyncIOMotorClient(settings.mongo_uri)
database = client[settings.db_name]
print(settings.db_name)
