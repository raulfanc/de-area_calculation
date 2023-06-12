"""
using `Spark` to handle large data, and `Prefect` to handle the workflow
"""


from datetime import timedelta
import math

from pyspark.sql import SparkSession, functions as F
from pyspark.sql import types as T

from prefect import task, flow
from prefect.tasks import task_input_hash


@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1)
def extract():
    # Start Spark session
    spark = SparkSession.builder \
        .master("local[*]") \
        .appName('plexure') \
        .getOrCreate()

    # Define schema
    schema = T.StructType([
        T.StructField("type", T.StringType(), True),
        T.StructField("width", T.DoubleType(), True),
        T.StructField("height", T.DoubleType(), True),
        T.StructField("base", T.DoubleType(), True),
        T.StructField("radius", T.DoubleType(), True)
    ])

    # Read JSON lines file into a DataFrame
    df = spark.read.json('dummy_data.jsonl', schema=schema, multiLine=False)

    return df


@task
def validate(df):
    # Filter the data using Spark SQL, `double` in schema doesn't convert negative value to null
    df = df.filter(
        (F.col('type') == 'rectangle' & F.col('width').isNotNull() & F.col('height').isNotNull() & F.col(
            'width') > 0 & F.col('height') > 0) |
        (F.col('type') == 'triangle' & F.col('base').isNotNull() & F.col('height').isNotNull() & F.col(
            'base') > 0 & F.col('height') > 0) |
        (F.col('type') == 'circle' & F.col('radius').isNotNull() & F.col('radius') > 0)
    )

    return df


@task
def calculate_area(df):
    # Add a new column "area" for each shape
    df = df.withColumn('area',
                       F.when(F.col('type') == 'rectangle', F.col('width') * F.col('height')) \
                       .when(F.col('type') == 'triangle', 0.5 * F.col('base') * F.col('height')) \
                       .when(F.col('type') == 'circle', math.pi * F.pow(F.col('radius'), 2))
                       )

    # Calculate the total area
    total_area = df.select(F.sum('area')).first()[0]

    return total_area


@flow()
def flowrun():
    df = extract()
    df_validated = validate(df)
    total_area = calculate_area(df_validated)
    print(total_area)


# Run the flow
if __name__ == "__main__":
    flowrun()
