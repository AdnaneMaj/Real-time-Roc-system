import json
from pathlib import Path
from models import MongoConfig
import ijson  # You'll need to install this package

# Create an instance of MongoConfig class
mongo = MongoConfig()

# Since PYTHONPATH=/app/src, this will point to /app/src
BASE_DIR = Path(__file__).parent

def chunk_iterator(items, chunk_size=1000):
    """Yield chunks of items with specified size."""
    chunk = []
    for item in items:
        chunk.append(item)
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []
    if chunk:  # Don't forget the last chunk
        yield chunk

def insert_data(collection_property, file_name, chunk_size=1000):
    """
    Insert data from a large JSON file into a MongoDB collection using streaming.
    
    Args:
        collection_property (str): The property name of the collection in MongoConfig.
        file_name (str): The name of the JSON file containing the data.
        chunk_size (int): Number of documents to insert in each batch.
    """
    try:
        file_path = BASE_DIR / file_name
        collection = getattr(mongo, collection_property)
        
        # Counter for progress tracking
        total_documents = 0
        
        with open(file_path, 'rb') as file:  # Open in binary mode for ijson
            # Assume the JSON file contains an array of objects
            parser = ijson.items(file, 'item')
            
            # Process the data in chunks
            for chunk in chunk_iterator(parser, chunk_size):
                collection.insert_many(chunk)
                total_documents += len(chunk)
                print(f'Inserted {total_documents} documents into {collection_property}')
                
        print(f'Completed inserting all data into {collection_property}')
        
    except Exception as e:
        print(f"Error inserting data into {collection_property}: {e}")

if __name__ == "__main__":
    insert_data('places_collection', 'places.json')
    insert_data('reviews_collection', 'reviews.json')