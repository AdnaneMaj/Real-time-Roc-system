import csv
from pathlib import Path
from models import MongoConfig

#Create an instance of MongoConfig class
mongo = MongoConfig()

# Since PYTHONPATH=/app/src, this will point to /app/src
BASE_DIR = Path(__file__).parent

# Insert data into 'places' collection
def insert_places():
    try:
        with open(BASE_DIR / 'places.csv', 'r') as file:
            reader = csv.DictReader(file)
            places = list(reader)
            mongo.places_collection.insert_many(places)
        print('Places data inserted')
    except Exception as e:
        print(f"Error inserting places: {e}")

# Insert data into 'reviews' collection
def insert_reviews():
    try:
        with open(BASE_DIR / 'reviews.csv', 'r') as file:
            reader = csv.DictReader(file)
            reviews = list(reader)
            mongo.reviews_collection.insert_many(reviews)
        print('Reviews data inserted')
    except Exception as e:
        print(f"Error inserting reviews: {e}")

# Call the functions to insert the data
if __name__ == "__main__":
    insert_places()
    insert_reviews()
