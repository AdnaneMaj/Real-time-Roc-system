from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str

    MONGODB_URL: str
    MONGODB_DATABASE: str

    KAFKA_URL: str

    REVIEW_COLLECTION_NAME: str
    AGGERATION_METRICS_COLLECTION_NAME: str
    PLACES_COLLECTION_NAME: str

    class Config:
        env_file = "./src/.env"

def get_settings():
    return Settings()