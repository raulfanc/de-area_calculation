"""
source_reader.py
responsible for reading data from the source file based on its extension
"""

import logging
from pathlib import Path
from pyspark.sql import SparkSession
from config import schema_config

# define the extensions for the source data
JSON_EXTENSIONS = ['.json', '.jsonl']
CSV_EXTENSIONS = ['.csv', '.gz']
PARQUET_EXTENSION = '.parquet'


def read_from_source(spark: SparkSession, input_path: str):
    try:
        file_ext = Path(input_path).suffix
        if file_ext in JSON_EXTENSIONS:
            df = spark.read.json(input_path, schema=schema_config, multiLine=False)
        elif file_ext in CSV_EXTENSIONS:
            df = spark.read.format('csv').option("header", "true").option("inferSchema", "true").load(input_path)
        elif file_ext == PARQUET_EXTENSION:
            df = spark.read.parquet(input_path)
        else:
            raise ValueError(f"Unsupported file extension {file_ext}")

        return df

    except Exception as e:
        logging.error(f"Data reading from source failed with error: {e}")
        raise
