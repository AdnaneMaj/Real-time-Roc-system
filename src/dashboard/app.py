import streamlit as st
from kafka import KafkaConsumer
import json
import pandas as pd

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
messages = st.empty()

# Function to process Kafka messages
def process_messages():
    for message in consumer:
        msg = message.value.decode()
        try:
            # Parse JSON message (if applicable)
            data = json.loads(msg)
            st.write(f"**Message:** {data}")

            # Display data in a table
            df = pd.DataFrame([data])
            st.table(df)

        except json.JSONDecodeError:
            st.write(f"**Raw Message:** {msg}")

# Run the message processing function
process_messages()