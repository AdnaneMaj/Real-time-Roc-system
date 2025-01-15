import csv
import pymongo
from pymongo import MongoClient

# MongoDB connection (use 'localhost' if running outside Docker)
  # Connect to MongoDB running on localhost
client = MongoClient('mongodb://mongo:27017/')  # 'mongo' is the service name in docker-compose.yml

db = client['projets']  # Replace with your actual database name

# Insert data into 'places' collection
def insert_places():
    try:
        with open('/src/places.csv', 'r') as file:
            reader = csv.DictReader(file)
            places = list(reader)
            db.places.insert_many(places)
        print('Places data inserted')
    except Exception as e:
        print(f"Error inserting places: {e}")

# Insert data into 'reviews' collection
def insert_reviews():
    try:
        with open('/src/reviews.csv', 'r') as file:
            reader = csv.DictReader(file)
            reviews = list(reader)
            db.reviews.insert_many(reviews)
        print('Reviews data inserted')
    except Exception as e:
        print(f"Error inserting reviews: {e}")

# Call the functions to insert the data
if __name__ == "__main__":
    insert_places()
    insert_reviews()
