import uuid
import json
import time
import requests
from kafka import KafkaProducer

def get_data():
    res = requests.get("https://randomuser.me/api/").json()
    return res['results'][0]

def format_data(res):
    location = res['location']
    return {
        'id': str(uuid.uuid4()),
        'first_name': res['name']['first'],
        'last_name': res['name']['last'],
        'gender': res['gender'],
        'address': f"{location['street']['number']} {location['street']['name']}, "
                   f"{location['city']}, {location['state']}, {location['country']}",
        'post_code': location['postcode'],
        'email': res['email'],
        'username': res['login']['username'],
        'dob': res['dob']['date'],
        'registered_date': res['registered']['date'],
        'phone': res['phone'],
        'picture': res['picture']['medium']
    }

def stream_data():
    producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)
    start_time = time.time()
    while time.time() - start_time < 60:  # Stream for 1 minute
        try:
            raw_data = get_data()
            formatted_data = format_data(raw_data)
            producer.send('users_created', json.dumps(formatted_data).encode('utf-8'))
            print(f"Sent: {formatted_data}")
            time.sleep(1)  # Throttle requests to avoid rate limiting
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    stream_data()



####################################################################################################################################""
#or

from kafka.streams import StreamsBuilder

def build_feature_topology(builder):
    # Create streams for different data sources
    location_stream = builder.stream('raw-location-data')
    weather_stream = builder.stream('weather-updates')
    sentiment_stream = builder.stream('sentiment-analysis-results')
    
    # Join streams and aggregate features
    enriched_stream = location_stream \
        .join(weather_stream, lambda loc, weather: merge_location_weather(loc, weather)) \
        .join(sentiment_stream, lambda enriched, sentiment: add_sentiment_features(enriched, sentiment))
    
    # Output aggregated features
    enriched_stream.to('feature-updates')