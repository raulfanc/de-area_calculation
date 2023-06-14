"""
Centralised configuration for Spark
- can add more settings here
"""

from pyspark.sql import SparkSession


def create_spark_session():
    """
    Create a SparkSession.
    """

    import os
    os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"

    spark = SparkSession.builder \
        .master("local[*]") \
        .appName('plexure') \
        .getOrCreate()

    print(f"SparkSession created with SparkContext ID {spark.sparkContext.applicationId}")
    print(f"Spark web UI available at {spark.sparkContext.uiWebUrl}")

    return spark


def stop_spark(spark):
    """
    Stop the SparkSession.
    """
    spark.stop()
