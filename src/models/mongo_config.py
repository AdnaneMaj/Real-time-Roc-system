from pymongo import MongoClient
from config.settings import get_settings
from geopy.distance import geodesic

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

    def get_nearby_places(self, user_lat, user_lon, max_distance_km=1):
        """
        Get nearby places to the user within a square area.
        """
        # Calculate the latitude and longitude boundaries for the square
        # 1 degree of latitude is approximately 111 km
        lat_delta = max_distance_km / 111
        lon_delta = max_distance_km / (111 * abs(user_lat))

        # Define the square boundaries
        min_lat = user_lat - lat_delta
        max_lat = user_lat + lat_delta
        min_lon = user_lon - lon_delta
        max_lon = user_lon + lon_delta

        # Query the database for places within the square
        query = {
            "latitude": {"$gte": min_lat, "$lte": max_lat},
            "longitude": {"$gte": min_lon, "$lte": max_lon},
        }
        nearby_places = self.places_collection.find(query)

        # Extract and return the names of nearby places
        return nearby_places
