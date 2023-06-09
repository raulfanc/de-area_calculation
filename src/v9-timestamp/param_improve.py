import math
from datetime import timedelta
import datetime
from datetime import datetime
import os
from pathlib import Path

from prefect import task, flow
from prefect.tasks import task_input_hash

from pyspark.sql import SparkSession, functions as F, types as T


timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
print_current_time = datetime.now().isoformat()


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

        df.write.parquet(parquet_path)

        print(f"Completed data extraction at {print_current_time}")
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
def write_data(df_valid, df_invalid, silver_valid_path, silver_invalid_path):
    print(f"Starting data writing at {datetime.now().isoformat()}")

    try:
        df_valid.write.json(os.path.join(silver_valid_path, f"valid_data_{timestamp}.jsonl"), mode="overwrite")
        df_invalid.write.json(os.path.join(silver_invalid_path, f"invalid_data_{timestamp}.jsonl"), mode="overwrite")

        print(f"Completed data writing at {datetime.now().isoformat()}")
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
def flow(input_path: str, parquet_path: str, silver_valid_path: str, silver_invalid_path: str, threshold: int):
    parquet_path = extract(input_path, parquet_path)
    df = read_data(parquet_path)
    df_valid, df_invalid = validate(df)
    total_area = calculate_area(df_valid)
    print(f"Total area: {total_area}")
    invalid_count = write_data(df_valid, df_invalid, silver_valid_path, silver_invalid_path)
    print(f"Invalid count: {invalid_count}")


if __name__ == "__main__":
    flow(
        input_path='dummy_data.jsonl',
        parquet_path='bronze/',
        silver_valid_path='silver/valid/',
        silver_invalid_path='silver/invalid/',
        threshold=5,
    )
