import math
import logging
from datetime import timedelta

from prefect import task, flow
from prefect.tasks import task_input_hash
from pyspark.sql import SparkSession, functions as F

from slack_notify import send_notification
from utils import get_timestamp, get_current_time, timed_path
from config import flow_param_config
from source_reader import read_from_source
from spark_config import create_spark_session, stop_spark

logging.basicConfig(level=logging.INFO)


@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract(spark, input_path: str, parquet_path: str):
    """
    Extract the data from a JSONL file and write it to a Parquet file.
    """
    try:
        df = read_from_source(spark, input_path)  # use the function from source_file_reader.py here
        df.write.parquet(parquet_path, mode='overwrite')
        print(f"Completed data extraction at {get_current_time()}")
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
        print(f"Total records at the beginning: {total_records}")  # debug
        return df, total_records
    except Exception as e:
        print(f"Data reading failed with error: {e}")
        raise


@task
def validate(df):
    print(f"Starting data validation at {get_current_time()}")

    # Define the valid types
    valid_types = ['rectangle', 'circle', 'triangle']

    # filter out the valid records
    valid_column = (
            (F.col('type').isin(valid_types)) &
            (F.when(F.col('type') == 'rectangle', (F.col('width') > 0) & (F.col('height') > 0))
             .otherwise(F.when(F.col('type') == 'circle', F.col('radius') > 0)
                        .otherwise(F.when(F.col('type') == 'triangle', (F.col('base') > 0) & (F.col('height') > 0))
                                   .otherwise(False))))
    )

    # Add the new column to tell valid and invalid records apart
    df = df.withColumn('isValid', valid_column)
    df_valid = df.filter(F.col('isValid'))
    df_invalid = df.filter(~F.col('isValid'))

    # debug
    print(f"Valid records: {df_valid.count()}")
    print(f"Invalid records: {df_invalid.count()}")

    print(f"Completed data validation at {get_current_time()}")

    return df_valid, df_invalid


@task
def write_data(df_valid, df_invalid, silver_valid_path, silver_invalid_path, invalid_rate, total_records):
    print(f"Starting data writing at {get_current_time()}")
    try:
        df_valid.write.json(timed_path(silver_valid_path, "valid_data", get_timestamp()), mode="overwrite")
        df_invalid.write.json(timed_path(silver_invalid_path, "invalid_data", get_timestamp()), mode="overwrite")
        print(f"Completed data writing at {get_current_time()}")

    except Exception as e:
        print(f"Data writing failed with error: {e}")
        raise

    invalid_count = df_invalid.count()

    # Notify on "Slack" if the invalid data threshold is reached
    if invalid_count / total_records * 100 >= invalid_rate:
        send_notification(
            f"Warning: The invalid data threshold has been reached. There were / "
            f"{invalid_count} invalid records out of {total_records} total records.")
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
    # start of the spark session
    spark = create_spark_session()
    # extract source and write to parquet, and saved in `bronze` folder (landing zone)
    parquet_path = extract(spark, input_path, parquet_path)
    # read data from landing zone, parquet is good with spark df
    df, total_records = read_data(spark, parquet_path)
    # validate data
    df_valid, df_invalid = validate(df)
    # calculate area
    calculate_area(df_valid)
    # write data to `silver` folder, separate valid and invalid with timestamp names
    write_data(df_valid, df_invalid, silver_valid_path, silver_invalid_path, invalid_rate, total_records)
    # stop_spark(spark)


if __name__ == "__main__":
    flow(**flow_param_config)       # go to `config.py` to control the flow parameters
