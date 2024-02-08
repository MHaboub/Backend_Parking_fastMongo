from motor.motor_asyncio import AsyncIOMotorClient
from configuration.conf import settings
mongo_uri: str = f"{settings.db_host}:{settings.db_port}"
client = AsyncIOMotorClient(mongo_uri)
database = client[settings.db_name]
print(settings.db_name)
