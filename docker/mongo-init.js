db = db.getSiblingDB('projets'); // Remplacez 'yourDatabaseName' par le nom de votre base de données

// Créer la collection 'places'
db.createCollection('places');

// Créer la collection 'reviews'
db.createCollection('reviews');
print("Collections 'places' et 'reviews' créées !");