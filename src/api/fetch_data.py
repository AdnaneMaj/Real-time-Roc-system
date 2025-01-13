import pandas as pd
import random

# Fonction pour ajouter une ligne au fichier CSV


names = [
    "Al Iman", "Al Fath", "An Nour", "Al Baraka", "As Salam", "Al Rahman", "Al Quds", "Al Hikma",
    "Ibn Khaldoun", "Al Idrissi", "Ibn Batouta", "Salah Eddine", "Al Mansour", "Ibn Rochd",
    "Atlas", "Sahara", "Rif", "Al Gharb", "Al Charq", "Toubkal", "Al Mazagan", "Mogador",
    "Al Malaki", "Al Sultani", "Al Amiri", "Al Wassim", "Al Bahia", "Al Saadi",
    "Al Wahat", "Al Nakhl", "Al Yasmine", "Al Ward", "Al Zaytoun", "Al Bahr"
]

regions = [
    "Tanger-Tetouan-Al Hoceima", "L'Oriental", "Fes-Meknes", "Rabat-Sale-Kenitra",
    "Beni Mellal-Khenifra", "Casablanca-Settat", "Marrakech-Safi", "Draa-Tafilalet",
    "Souss-Massa", "Guelmim-Oued Noun", "Laayoune-Sakia El Hamra", "Dakhla-Oued Ed-Dahab"
]

place_types = [
    "Beach", "Historical monument", "Museum", "Medina", "Mosque", "Market",
    "Natural park", "Archaeological site", "Kasbah", "Palace", "Garden",
    "Public square", "Mountain", "Oasis", "Cave", "Port", "Marina",
    "Thermal baths", "Hammam", "Craft center"
]

categories = [
    "Cultural", "Natural", "Historical", "Religious", "Craft",
    "Seaside", "Mountainous", "Desert", "Urban", "Rural"
]

activities = [
    "Guided tour", "Hiking", "Photography", "Shopping", "Swimming",
    "Surfing", "Climbing", "Skiing", "Camping", "Bird watching",
    "Craft making", "Gastronomy", "Meditation", "Water sports", "Fishing"
]

comments = [
    "A must-visit place for history enthusiasts!",
    "Poorly maintained and not worth the visit.",
    "Too crowded and noisy.",
    "Rich in culture and traditions.",
    "Ideal for family outings and relaxation.",
    "Overpriced for what it offers.",
    "Stunning views and breathtaking scenery.",
    "The place was dirty and not well-organized.",
    "Limited activities and things to do.",
    "Highly recommended for food lovers.",
    "Unique, it contains unique activities and experiences.",
    "Lack of parking facilities.",
    "Perfect spot for adventure lovers.",
    "Not accessible for people with disabilities.",
    "Great location for photography.",
    "Difficult to find and poorly signposted.",
    "A peaceful place to unwind.",
    "The staff was unhelpful and rude.",
    "A disappointing experience.",
    "The best visited during the sunny season."
]

# Function to generate a random price


def generate_price():
    return round(random.uniform(0, 500), 2)

# Function to generate coordinates in Morocco


def generate_coordinates():
    lat = random.uniform(27.6666, 35.9234)  # Morocco latitude range
    lon = random.uniform(-13.1686, -1.0347)  # Morocco longitude range
    return (round(lat, 4), round(lon, 4))

# Function to generate opening hours


def generate_opening_hours():
    opening = random.randint(7, 10)
    closing = random.randint(17, 23)
    return f"{opening:02d}:00-{closing:02d}:00"

# Data generator function


def generate_tourist_data():
    lat, lon = generate_coordinates()
    place_type = random.choice(place_types)
    category = random.choice(categories)
    record = {
        "region": random.choice(regions),
        "type": place_type,
        "name": f"{place_type} {random.choice(names)}",
        "category": category,
        "latitude": lat,
        "longitude": lon,
        "entry_fee": generate_price(),
        "opening_hours": generate_opening_hours(),
        "available_activities": random.sample(activities, random.randint(1, 5)),
        "wheelchair_accessible": random.choice([True, False]),
        "parking_available": random.choice([True, False]),
        "max_capacity": random.randint(50, 5000),
        "average_visit_duration": random.randint(30, 480),
        "weather": random.sample(["sunny", "windy", "cold", "rainy"], random.randint(1, 4)),
        "languages_available": random.sample(["Arabic", "French", "English", "Spanish", "German"], random.randint(1, 5)),
        "comment": f"{place_type} is {random.choice(comments)}"
    }
    return record

# Fonction pour obtenir la localisation de l'utilisateur


def user_location():
    return generate_coordinates()

# Fonction pour obtenir les préférences météo de l'utilisateur


def user_weather():
    return random.choice(["sunny", "windy", "rainy", "cold"])