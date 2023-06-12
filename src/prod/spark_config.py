"""
Centralised configuration for Spark
- can add more settings here
"""

from pyspark.sql import SparkSession


def create_spark_session():
    """
    Create a SparkSession.
    """
    spark = SparkSession.builder \
        .master("local[*]") \
        .appName('plexure') \
        .getOrCreate()

    return spark


def stop_spark(spark):
    """
    Stop the SparkSession.
    """
    spark.stop()
