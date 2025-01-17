import streamlit as st
from kafka import KafkaConsumer
import json
import pandas as pd
import time

# Streamlit app title
st.title("Kafka Consumer Dashboard - Weather Topic")

# Initialize Kafka consumer
consumer = KafkaConsumer(
    'weather-topic',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    group_id='my-group'
)

# Placeholder for messages
message_placeholder = st.empty()
table_placeholder = st.empty()

# Function to process Kafka messages
def process_messages():
    for message in consumer:
        msg = message.value.decode()
        try:
            # Parse JSON message (if applicable)
            data = json.loads(msg)
            message_placeholder.write(f"**Latest Message:** {data}")

            # Display data in a table
            df = pd.DataFrame([data])
            table_placeholder.table(df)

        except json.JSONDecodeError:
            message_placeholder.write(f"**Raw Message:** {msg}")

        time.sleep(1)

# Run the message processing function
process_messages()