from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorCollection
from config.settings import get_settings

class MongoConfig:
    def __init__(self):
        self.app_setting = get_settings()
        self.client = AsyncIOMotorClient(self.app_setting.MONGODB_URL)
        self.db = self.client[self.app_setting.MONGODB_DATABASE]

    @property
    def places_collection(self) -> AsyncIOMotorCollection:
        return self.db[self.app_setting.PLACES_COLLECTION_NAME]

    @property
    def reviews_collection(self) -> AsyncIOMotorCollection:
        return self.db[self.app_setting.REVIEW_COLLECTION_NAME]
    
    @property
    def agregaton_metrics(self) -> AsyncIOMotorCollection:
        return self.db[self.app_setting.AGGERATION_METRICS_COLLECTION_NAME]
