from pymongo import MongoClient
from config.settings import get_settings

class MongoConfig:
    def __init__(self):
        self.app_setting = get_settings()
        self.client = MongoClient(self.app_setting.MONGODB_URL)
        self.db = self.client[self.app_setting.MONGODB_DATABASE]

    @property
    def places_collection(self):
        return self.db[self.app_setting.PLACES_COLLECTION_NAME]

    @property
    def reviews_collection(self):
        return self.db[self.app_setting.REVIEW_COLLECTION_NAME]

    @property
    def aggregation_metrics(self):
        return self.db[self.app_setting.AGGERATION_METRICS_COLLECTION_NAME]
