"""

Some function that generate random data when invoced :

- get_temperature

"""
import random
import numpy as np
from typing import Dict

class API:

    Weather_list = ['sunny','wendy','rainy']
    
    def __init__(self):
        self.user_location = np.array([33.98,-6.86]) #initalise the user location in rabat ( ensias exactly )

    def get_location(self):
        """
        Approximate Geographic Limits of Morocco:
            Latitude Range: 21.33°N to 35.92°N
            Longitude Range: -13.17°W to -1.02°W
        """
        step = np.random.rand(2,)*0.01

        self.user_location += step #The user makes a step

    def get_weather(self)->str:
        #retrun a random weather
        
        return random.choice(API.Weather_list.choice())
    
    def get_data_row(self) -> Dict:
        """
        Get a row of the data as dict just like 
        """
        
        #data randomly
        row = {
            "id": 1,
            "name": "Site touristique 1",
            "region": "Rabat-Salé-Kénitra",
            "category": "Kasbah",
            "type": "Religieux",
            "latitude": 30.7845,
            "longitude": -1.4069,
            "altitude": 484.68,
            "rating": 4.1,
            "reviews_count": 47,
            "opening_hours": "08:00-21:00",
            "activities": ['Camping', "Observation d'oiseaux", 'Pêche', 'Sport nautique', 'Shopping'],
            "accessible": True,
            "family_friendly": False,
            "visitors_count": 639,
            "price_range": 98,
            "popularity": "Moyen",
            "weather": 'sunny',
            "languages": ['Allemand', 'Arabe'],
            "reviews": [
                "Site touristique 1 is okay for a short visit. Some activities are fun, but I wasn’t fully impressed.",
                "Site touristique 1 was fine, but it didn’t blow me away. The activities like 'Camping', \"Observation d'oiseaux\", 'Pêche', 'Sport nautique', 'Shopping' were decent, but service could be better.",
                "Site touristique 1 offers a pleasant experience, but some areas could use improvement. Worth a visit if you’re nearby.",
                "Not bad overall! Site touristique 1 has potential, but the facilities need a bit of work to really shine."
            ]
        }

        return row
