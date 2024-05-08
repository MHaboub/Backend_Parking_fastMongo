from motor.motor_asyncio import AsyncIOMotorClient
from configuration.conf import settings
# mongo_uri: str = f"{settings.db_host}:{settings.db_port}"
m="mongodb+srv://admin:1234!@parking.6eatiz9.mongodb.net/?retryWrites=true&w=majority"
print(settings.db_host)
client = AsyncIOMotorClient(settings.db_host)
database = client[settings.db_name]
print(settings.db_host)
