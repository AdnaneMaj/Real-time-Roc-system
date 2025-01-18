import random
#from transformers import BertTokenizer, BertForSequenceClassification
#import torch
import math
import time
import json

class UserLocalization:
    def __init__(self):
        """
        Initialize the user's location.

        :param localisation: Tuple representing (latitude, longitude) in degrees.
        """
        self.localisation = UserLocalization.generate_coordinates()  # Initialise the user position (latitude, longitude) randomly in morroco ( or another country )
        self.speed_mps = 1.0  # Speed in meters per second (1 m/s)

    @staticmethod
    def generate_coordinates():
        lat = 34.4266787  # a place in morroco
        lon = -119.7111968  
        return (round(lat, 4), round(lon, 4))

    def update_position(self, direction_angle=45):
        """
        Update the user's position based on a movement direction angle.

        :param direction_angle: Angle in degrees, where 0 is north, 90 is east, 180 is south, and 270 is west.
        """
        # Convert angle to radians
        angle_rad = math.radians(direction_angle)

        # Earth's radius in meters
        earth_radius = 6371000

        # Current latitude and longitude in radians
        lat_rad = math.radians(self.localisation[0])
        lon_rad = math.radians(self.localisation[1])

        # Calculate new latitude and longitude in radians
        delta_lat = self.speed_mps / earth_radius * math.cos(angle_rad)
        delta_lon = self.speed_mps / (earth_radius * math.cos(lat_rad)) * math.sin(angle_rad)

        new_lat_rad = lat_rad + delta_lat
        new_lon_rad = lon_rad + delta_lon

        # Convert back to degrees
        new_lat = math.degrees(new_lat_rad)
        new_lon = math.degrees(new_lon_rad)

        # Update the position
        self.localisation = (new_lat, new_lon)

#___________________________________________________________________________________________________________
"""
This function is totay prerfect, it's just that i have a problem with docker, transfoerms and torch packages take too much time to be installed which increases heavily the build time
"""
def generate_score(comment):
    """
    model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name)
    inputs = tokenizer(comment, return_tensors="pt",
                       truncation=True, padding=True, max_length=512)

    # 3. Obtenir les prédictions
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    # 4. Convertir les logits en scores
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    score = torch.argmax(probabilities).item()  # Catégorie prédite
    confidence = probabilities[0, score].item()  # Confiance associée
    """

    score = 0
    return score


if __name__=="__main__":
    from kafka import KafkaProducer
    import random

    producer = KafkaProducer(
        bootstrap_servers = 'kafka:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')  # JSON serialization
    )

    user = UserLocalization() #Iitialise a user
    latitude, longitude = user.localisation

    print("User crated, initial localsiation")
    
    while True:
        user_localisation = user.localisation

        producer.send('localisation-topic', user_localisation)
        print(f"User now is in position : {user_localisation}")
        print("Message sent!")

        #update position each second
        time.sleep(0.2)
        user.update_position()