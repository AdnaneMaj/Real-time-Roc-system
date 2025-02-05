import json
from kafka import KafkaConsumer
import streamlit as st
from models import MongoConfig
from datetime import datetime
from collections import OrderedDict

# Set the MongoDB connection
mongodb = MongoConfig()

def format_place_card(place):
    return f"""
    <div style="
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        min-height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    ">
        <h3 style="color: #1f1f1f; margin: 0 0 10px 0;">{place['name']}</h3>
        <div style="color: #666;">
            <p style="margin: 5px 0;">Type: {place.get('type', 'N/A')}</p>
            <p style="margin: 5px 0;">Distance: {place.get('distance', 'N/A')} m</p>
        </div>
    </div>
    """

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
        col1.metric("Latitude", f"{latitude:.6f}")
        col2.metric("Longitude", f"{longitude:.6f}")
        
        if nearby_places:
            st.subheader("Nearby Places (within 1km)")
            
            # Update the places history in session state
            if 'places_history' not in st.session_state:
                st.session_state.places_history = OrderedDict()
            
            # Add new places to history with timestamp
            current_time = datetime.now()
            for place in nearby_places:
                place_id = place.get('id', str(place))  # Use a unique identifier
                st.session_state.places_history[place_id] = {
                    'place': place,
                    'timestamp': current_time
                }
            
            # Keep only the 10 most recent unique places
            if len(st.session_state.places_history) > 10:
                # Remove oldest entries until we have 10
                while len(st.session_state.places_history) > 10:
                    st.session_state.places_history.popitem(last=False)
            
            # Create a grid layout for places
            places_html = '<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px;">'
            
            for place_data in st.session_state.places_history.values():
                places_html += format_place_card(place_data['place'])
            
            places_html += '</div>'
            
            # Display the grid using HTML
            st.markdown(places_html, unsafe_allow_html=True)
        else:
            st.warning("No nearby places found.")
        
        st.success(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    except (json.JSONDecodeError, ValueError) as e:
        st.error(f"Error processing message: {e}")

def consume_kafka_messages():
    consumer = KafkaConsumer(
        "localisation-topic",
        bootstrap_servers=['kafka:9092'],
        value_deserializer=lambda x: x.decode("utf-8"),
    )
    
    for message in consumer:
        # Process the Kafka message
        process_localization_data(message)
        
        # Rerun the app to update the UI
        st.rerun()

if __name__ == '__main__':
    # Initialize session state for places history
    if 'places_history' not in st.session_state:
        st.session_state.places_history = OrderedDict()
    
    # Streamlit dashboard
    dashboard("consumer")
    
    # Consume Kafka messages
    consume_kafka_messages()