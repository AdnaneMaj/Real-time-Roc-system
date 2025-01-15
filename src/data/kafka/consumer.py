from kafka import KafkaConsumer
import json

def consume_from_kafka(topic):
    global current_weather
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='kafka:9092',
        value_deserializer=lambda v: v.decode('utf-8')
    )
    for message in consumer:
        try:
            data = json.loads(message.value)
            current_weather = data['weather']
        except:
            current_weather = "Error reading weather"
