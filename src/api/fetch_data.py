import random
#from transformers import BertTokenizer, BertForSequenceClassification
#import torch
from pymongo import MongoClient
import time

# Fonction pour ajouter une ligne au fichier CSV
model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)


client = MongoClient('mongodb://localhost:27017/')  # Remplacez localhost par "mongo" si Docker
db = client['projets'] 

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
    "Unique activities and experiences.",
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


def generate_place():
    lat, lon = generate_coordinates()
    place_type = random.choice(place_types)
    category = random.choice(categories)
    id = random.randint(1, 50000)
    record = {
        "place_id": id,
        "region": random.choice(regions),
        "type": place_type,
        "name": f"Place_{id}",
        "category": category,
        "longitude": lon,
        "latitude": lat,
        "opening_hours": generate_opening_hours(),
        "entry_fee": generate_price(),
        "available_activities": random.sample(activities, random.randint(1, 5)),
        "wheelchair_accessible": random.choice([True, False]),
        "parking_available": random.choice([True, False]),
        "max_capacity": random.randint(50, 5000),
        "weather": random.choice(["sunny", "windy", "cold", "rainy"]),
        "language_available": random.sample(["Arabic", "French", "English", "Spanish", "German"], random.randint(1, 5)),
        "average_visit_duration": random.randint(30, 480),
    }
    return record
# Fonction pour générer les commentaires


def generate_comment():
    comment = random.choice(comments)
    review = {
        "place_id": random.randint(1, 50000),
        "comment": comment,
        "sentiment_score": generate_score(comment)
    }
    return review
# générer un score


def generate_score(comment):
    # Ex. modèle de sentiment
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
    return score


# Fonction pour obtenir la localisation de l'utilisateur

def user_location():
    return generate_coordinates()

# Fonction pour obtenir les préférences météo de l'utilisateur


def user_weather():
    return random.choice(["sunny", "windy", "rainy", "cold"])
  
def insert_data_realtime():
    try:
        while True:
            # Générer un document pour places et reviews
            place = generate_place()
            review = generate_comment()

            # Insérer dans les collections
            db.places.insert_one(place)
            db.reviews.insert_one(review)

            print(f"Inserted place: {place['name']}, review sentiment: {review['sentiment_score']}")
            
            # Attendre avant la prochaine insertion
            time.sleep(60)  # Modifier le délai en secondes si nécessaire
    except Exception as e:
        print(f"Error during real-time insertion: {e}")


if __name__=="__main__":
    from kafka import KafkaProducer
    import random

    producer = KafkaProducer(bootstrap_servers = 'kafka:9092')


    while True:
        #Insert incoming data
        insert_data_realtime()
        
        #Get weather
        msg = user_weather()
        producer.send('weather-topic', msg.encode('utf-8'))
        print("The weather is : \"{}\"".format(msg))
        print("Message sent!")
