import json
from kafka import KafkaConsumer
import streamlit as st
from models import MongoConfig

# Set the MongoDB connection
mongodb = MongoConfig()

# Streamlit app
def dashboard(dashboard_type: str):
    # Default settings
    st.set_page_config(
        page_title="Real-time User Localization App",
        page_icon="📍",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Run the Streamlit app
    st.title(str.upper(dashboard_type) + " : User Localization")


    # Sidebar with user instructions
    st.sidebar.markdown(
        """
        This app fetches real-time user localization data from Kafka messages.
        It displays the latest user location and nearby places within a 1km radius.
        """
    )

    # Display localization data in the main section
    st.header("Real-Time User Localization with Kafka + Streamlit")


# Process localization data from Kafka message
def process_localization_data(message):
    try:
        # Parse the JSON message
        data = json.loads(message.value)

        # Validate the message structure
        if not isinstance(data, list) or len(data) != 2:
            raise ValueError("Invalid message format. Expected [latitude, longitude].")

        latitude, longitude = data

        # Fetch nearby places from the database
        nearby_places = mongodb.get_nearby_places(latitude, longitude, max_distance_km=1)

        # Update the Streamlit app with the localization data
        col1, col2 = st.columns(2)
        col1.metric("Latitude", latitude)
        col2.metric("Longitude", longitude)

        if nearby_places:
            st.subheader("Nearby Places (within 1km)")
            for place in nearby_places:
                st.write(f"- {place}")
        else:
            st.warning("No nearby places found.")

        st.success(f"Last updated: {st.session_state.last_updated}")

    except (json.JSONDecodeError, ValueError) as e:
        st.error(f"Error processing message: {e}")


# Function to consume messages from Kafka topic
def consume_kafka_messages():
    consumer = KafkaConsumer(
        "localisation-topic",
        bootstrap_servers=['kafka:9092'],
        value_deserializer=lambda x: x.decode("utf-8"),
    )

    for message in consumer:
        # Update the last updated timestamp
        st.session_state.last_updated = st.session_state.get("last_updated", "N/A")

        # Process the Kafka message
        process_localization_data(message)

        # Rerun the app to update the UI
        st.rerun()


# Update the Streamlit app with data from the background thread
if __name__ == '__main__':
    # Initialize session state for last updated timestamp
    if "last_updated" not in st.session_state:
        st.session_state.last_updated = "N/A"

    # Streamlit dashboard
    dashboard("consumer")

    # Consume Kafka messages
    consume_kafka_messages()