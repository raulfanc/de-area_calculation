from datetime import timedelta
import os
import datetime
import math

from prefect import task, flow
from prefect.tasks import task_input_hash

from pyspark.sql import SparkSession, functions as F, types as T


@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract(input_path: str, parquet_path: str):
    """
    Extract the data from a JSONL file and write it to a Parquet file.
    """
    spark = SparkSession.builder \
        .master("local[*]") \
        .appName('plexure') \
        .getOrCreate()

    schema = T.StructType([
        T.StructField("type", T.StringType(), True),
        T.StructField("width", T.DoubleType(), True),
        T.StructField("height", T.DoubleType(), True),
        T.StructField("base", T.DoubleType(), True),
        T.StructField("radius", T.DoubleType(), True)
    ])

    print(f"Starting data extraction from {input_path} at {datetime.datetime.now().isoformat()}")

    try:
        df = spark.read.json(input_path, schema=schema, multiLine=False)
        df.write.parquet(parquet_path)

        print(f"Completed data extraction at {datetime.datetime.now().isoformat()}")
        return parquet_path
    except Exception as e:
        print(f"Data extraction failed with error: {e}")
        raise


@task
def read_data(parquet_path: str):
    """
    Read the data from a Parquet file.
    """
    spark = SparkSession.builder \
        .master("local[*]") \
        .appName('plexure') \
        .getOrCreate()

    try:
        df = spark.read.parquet(parquet_path)
        return df
    except Exception as e:
        print(f"Data reading failed with error: {e}")
        raise


@task
def validate(df):
    print(f"Starting data validation at {datetime.datetime.now().isoformat()}")

    df_valid = df.filter(
        ((F.col('type') == 'rectangle') & F.col('width').isNotNull() & F.col('height').isNotNull()) |
        ((F.col('type') == 'triangle') & F.col('base').isNotNull() & F.col('height').isNotNull()) |
        ((F.col('type') == 'circle') & F.col('radius').isNotNull())
    )

    df_invalid = df.subtract(df_valid)

    print(f"Completed data validation at {datetime.datetime.now().isoformat()}")

    return df_valid, df_invalid


@task
def write_data(df_valid, df_invalid, output_path, invalid_data_path):
    print(f"Starting data writing at {datetime.datetime.now().isoformat()}")

    try:
        df_valid.write.json(os.path.join(output_path, "valid_data.jsonl"), mode="overwrite")
        df_invalid.write.json(os.path.join(invalid_data_path, "invalid_data.jsonl"), mode="overwrite")

        print(f"Completed data writing at {datetime.datetime.now().isoformat()}")
    except Exception as e:
        print(f"Data writing failed with error: {e}")
        raise

    invalid_count = df_invalid.count()

    return invalid_count


@task
def calculate_area(df):
    df = df.withColumn('area',
                       F.when(F.col('type') == 'rectangle', F.col('width') * F.col('height')) \
                       .when(F.col('type') == 'triangle', 0.5 * F.col('base') * F.col('height')) \
                       .when(F.col('type') == 'circle', math.pi * F.pow(F.col('radius'), 2))
                       )
    total_area = df.select(F.sum('area')).first()[0]

    return total_area


@flow()
def flow(input_path: str, parquet_path: str, output_path: str, invalid_data_path: str, threshold: int):
    parquet_path = extract(input_path, parquet_path)
    df = read_data(parquet_path)
    df_valid, df_invalid = validate(df)
    total_area = calculate_area(df_valid)
    print(f"Total area: {total_area}")
    invalid_count = write_data(df_valid, df_invalid, output_path, invalid_data_path)
    print(f"Invalid count: {invalid_count}")


if __name__ == "__main__":
    flow(
        input_path='dummy_data.jsonl',
        parquet_path='raw',
        output_path='silver',
        invalid_data_path='invalid',
        threshold=10
    )