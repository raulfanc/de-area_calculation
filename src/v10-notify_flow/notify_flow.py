import math
from datetime import timedelta
import datetime
from datetime import datetime
from pathlib import Path
import os

from prefect import task, flow
from prefect.tasks import task_input_hash

from pyspark.sql import SparkSession, functions as F, types as T

from slack_notify import send_notification

timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
print_current_time = datetime.now().isoformat()


@task
def create_spark_session():
    """
    Create a SparkSession.
    """
    spark = SparkSession.builder \
        .master("local[*]") \
        .appName('plexure') \
        .getOrCreate()

    return spark


@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract(spark, input_path: str, parquet_path: str):
    """
    Extract the data from a JSONL file and write it to a Parquet file.
    """

    schema = T.StructType([
        T.StructField("type", T.StringType(), True),
        T.StructField("width", T.DoubleType(), True),
        T.StructField("height", T.DoubleType(), True),
        T.StructField("base", T.DoubleType(), True),
        T.StructField("radius", T.DoubleType(), True)
    ])

    print(f"Starting data extraction from {input_path} at {print_current_time}")

    try:
        file_ext = Path(input_path).suffix
        # if the file_ext is json or jsonl, then use the schema
        if file_ext in ['.json', '.jsonl']:
            df = spark.read.json(input_path, schema=schema, multiLine=False)
        elif file_ext in ['.csv', '.gz']:
            df = spark.read.format('csv').option("header", "true").option("inferSchema", "true").load(input_path)
        elif file_ext == '.parquet':
            df = spark.read.parquet(input_path)
        else:
            raise ValueError(f"Unsupported file extension {file_ext}")

        df.write.parquet(parquet_path, mode='overwrite')

        print(f"Completed data extraction at {print_current_time}")
        return parquet_path
    except Exception as e:
        print(f"Data extraction failed with error: {e}")
        raise


@task
def read_data(spark, parquet_path: str):
    """
    Read the data from a Parquet file.
    """

    try:
        df = spark.read.parquet(parquet_path)
        total_records = df.count()
        return df, total_records
    except Exception as e:
        print(f"Data reading failed with error: {e}")
        raise


@task
def validate(df):
    print(f"Starting data validation at {print_current_time}")

    df_valid = df.filter(
        ((F.col('type') == 'rectangle') & F.col('width').isNotNull() & F.col('height').isNotNull()) |
        ((F.col('type') == 'triangle') & F.col('base').isNotNull() & F.col('height').isNotNull()) |
        ((F.col('type') == 'circle') & F.col('radius').isNotNull())
    )

    df_invalid = df.subtract(df_valid)

    print(f"Completed data validation at {print_current_time}")

    return df_valid, df_invalid


@task
def write_data(df_valid, df_invalid, silver_valid_path, silver_invalid_path, invalid_rate, total_records):
    print(f"Starting data writing at {datetime.now().isoformat()}")

    try:
        df_valid.write.json(os.path.join(silver_valid_path, f"valid_data_{timestamp}.jsonl"), mode="overwrite")
        df_invalid.write.json(os.path.join(silver_invalid_path, f"invalid_data_{timestamp}.jsonl"), mode="overwrite")

        print(f"Completed data writing at {datetime.now().isoformat()}")
    except Exception as e:
        print(f"Data writing failed with error: {e}")
        raise

    invalid_count = df_invalid.count()

    # Send a message to Slack if the invalid data threshold is reached
    if invalid_count / total_records * 100 >= invalid_rate:
        send_notification(
            f"Warning: The invalid data threshold has been reached. There were / "
            f"{invalid_count} invalid records out of {total_records} total records.")
    print(f"Invalid count: {invalid_count}")
    return invalid_count


@task
def calculate_area(df):
    df = df.withColumn('area',
                       F.when(F.col('type') == 'rectangle', F.col('width') * F.col('height')) \
                       .when(F.col('type') == 'triangle', 0.5 * F.col('base') * F.col('height')) \
                       .when(F.col('type') == 'circle', math.pi * F.pow(F.col('radius'), 2))
                       )
    total_area = df.select(F.sum('area')).first()[0]

    print(f"Total area: {total_area}")
    return total_area


@flow()
def flow(input_path: str, parquet_path: str, silver_valid_path: str, silver_invalid_path: str, invalid_rate: int):
    spark = create_spark_session()
    parquet_path = extract(spark, input_path, parquet_path)
    df, total_records = read_data(spark, parquet_path)
    df_valid, df_invalid = validate(df)
    calculate_area(df_valid)
    write_data(df_valid, df_invalid, silver_valid_path, silver_invalid_path, invalid_rate, total_records)


if __name__ == "__main__":
    flow(
        input_path='dummy_data.jsonl',
        parquet_path='bronze/',
        silver_valid_path='silver/valid/',
        silver_invalid_path='silver/invalid/',
        invalid_rate=5,
    )
