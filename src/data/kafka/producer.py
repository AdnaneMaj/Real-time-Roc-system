from kafka import KafkaProducer
import json

# Initialize the Kafka producer once
shared_producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize dict to JSON string
)

def send_to_kafka(topic, data):
    """
    Sends a message to a Kafka topic using a shared producer instance.
    """
    shared_producer.send(topic, value=data)
