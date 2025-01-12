import pandas as pd
import random

# Fonction pour ajouter une ligne au fichier CSV


def data_place():
    new_place = {
        "region": random.choice(["Rabat-Salé-Kénitra", "L'Oriental", "Marrakech-Safi"]),
        "type": random.choice(["Kasbah", "Marina", "Thermes", "Parc naturel"]),
        "categorie": random.choice(["Religieux", "Urbain", "Naturel", "Culturel"]),
        "latitude": round(random.uniform(27.0, 35.0), 4),
        "longitude": round(random.uniform(-13.0, -1.0), 4),
        "prix_entree": round(random.uniform(50, 500), 2),
        "note_moyenne": round(random.uniform(3.5, 5.0), 1),
        "nombre_avis": random.randint(50, 10000),
        "horaires": "08:00-20:00",
        "activites_disponibles": random.choice(["Camping", "Randonnée", "Observation d'oiseaux"]),
        "accessible_handicap": random.choice([True, False]),
        "parking_disponible": random.choice([True, False]),
        "capacite_max": random.randint(100, 5000),
        "temps_visite_moyen": random.randint(30, 500),
        "meilleure_periode": random.choice(["sunny", "windy", "rainy", "cold"]),
        "langues_visites": random.choice(["Arabe", "Français", "Anglais", "Espagnol"])
    }
    return new_place

# Fonction pour obtenir la localisation de l'utilisateur


def user_location():
    # Simuler une localisation au Maroc
    latitude = round(random.uniform(27.0, 35.0), 4)
    longitude = round(random.uniform(-13.0, -1.0), 4)
    return latitude, longitude

# Fonction pour obtenir les préférences météo de l'utilisateur


def user_weather():
    return random.choice(["sunny", "windy", "rainy", "cold"])
