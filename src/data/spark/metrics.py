from pyspark.sql import SparkSession
from pyspark.sql.functions import avg

def calculate_metrics():
    spark = SparkSession.builder \
        .appName("RecommenderSystem") \
        .getOrCreate()

    # Load reviews data from MongoDB
    reviews_df = spark.read \
        .format("mongo") \
        .option("uri", "mongodb://mongo:27017/recommender_system.reviews") \
        .load()

    # Calculate mean rating per place
    metrics_df = reviews_df.groupBy("place_id").agg(avg("rating").alias("mean_rating"))

    # Save metrics to MongoDB
    metrics_df.write \
        .format("mongo") \
        .option("uri", "mongodb://mongo:27017/recommender_system.metrics") \
        .mode("overwrite") \
        .save()