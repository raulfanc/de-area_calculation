# Shape Calculator Challenge

The application should calculate the total area of all the shapes in the data set.
```json lines
{"type": "rectangle", "width": 5, "height": 10}
{"type": "triangle", "base": 2, "height": 3}
{"type": "circle", "radius": 4}
{"type": "rectangle", "width": 5, "height": 5}
```
---
## Run Code
- all development included in [src](./src/) folder, contains 10 versions.
- each version has its own README.md, can run the python code directly.
- between v1 and v6, use [requirements.txt](./requirements.txt) to install packages.
- [jsonl_generator.py](/src/v7-spark/jsonl_generator.py) is used to generate more jsonl (with some random bad data) for testing purpose.
- from v7, by using `spark`, moving development to google vm, install the [requirements.txt](./requirements.txt) on the vm
- follow [spark_install.md](./src/v7-spark/spark_install.md)


prod code 
prod code is at [src/prod](./src/prod)
1. slack notification is at [src/prod/slack_notify.py](./src/prod/slack_notify.py)
2. to get slack work, need api key and a few dependencies, refer to [prod_README](./src/prod/README.md)

---

## Objectives
- what quality software looks like: modular, maintainable, extensible, scalable.
- highlighting in Data Engineering: Prefect, Spark, Data Quality validation, logging, monitoring.

## Requirements
- data wrangling with `Spark`
- modularity with `Prefect`

## Development Journey
![flow chart](https://docs.google.com/drawings/d/1SGDb3KNLXFSUYwWvO6a0qC8zgM7em-NQSCHKC3uap-w/export/png)

## Data Pipeline
![data pipeline](https://docs.google.com/drawings/d/1xLOXTJa-m3XjzWLJRbIeHF4H7oYp-hqi3qMAA1fc91s/export/png)

## Application
- ingest data that represents various geometric shapes (currently rectangles, triangles, and circles, but the solution should be extensible for more shapes in the future).

- modular designed to handle different data sources (e.g. API calls, JSONs, Parquet, CSVs etc.).

- can handle big data ingest with retries and error handling (connection issue, data quality issue, etc.).

- have designed data storage for different quality data (e.g. raw, clean, invalid, etc.).

- The application should calculate and return the total area of all the shapes in the valid_data set.


## todo
- [spark_config.py](./src/prod/spark_config.py) reserved to change the spark configuration

- unit-testable, preferably using the `Pytest`

- parallel ingesting (concurrent)

- more validation on the different stages

- explicitly and more specific about the error-handling

- logging instead of print




Act as a senior data engineer, help me to re-write the `validate task`, requirements:
# problem 1: below the data loads into `validate task`, it has 2 steps prior, first step is extract the data into parquet format, and second step is to read parquet data and load into spark dataframe, see code below :
```main.py
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
df = read_from_source(spark, input_path) # use the function from source_file_reader.py here  
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
print(f"Total records at the beginning: {total_records}") # debug  
return df, total_records  
except Exception as e:  
print(f"Data reading failed with error: {e}")  
raise  
  
  
@task  
def validate(df):  
print(f"Starting data validation at {get_current_time()}")  
  
print(f"Total records before validation: {df.count()}") # debug  
  
df_valid = df.filter(  
((F.col('type') == 'rectangle') & F.col('width').cast('double').isNotNull() & F.col('height').cast('double').isNotNull() & (F.col('width') > 0) & (F.col('height') > 0)) |  
((F.col('type') == 'triangle') & F.col('base').cast('double').isNotNull() & F.col('height').cast('double').isNotNull() & (F.col('base') > 0) & (F.col('height') > 0)) |  
((F.col('type') == 'circle') & F.col('radius').cast('double').isNotNull() & (F.col('radius') > 0))  
)  
  
df_invalid = df.subtract(df_valid)  
  
print(f"Valid records: {df_valid.count()}") # debug  
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
spark = create_spark_session()  
parquet_path = extract(spark, input_path, parquet_path)  
df, total_records = read_data(spark, parquet_path)  
df_valid, df_invalid = validate(df)  
calculate_area(df_valid)  
write_data(df_valid, df_invalid, silver_valid_path, silver_invalid_path, invalid_rate, total_records)  
stop_spark(spark)  
  
  
if __name__ == "__main__":  
flow(**flow_param_config)
```

and the main.py uses the module source_reader.py for extract task when loading different ext files, in this test, we are feeding the jsonl format
```source_reader.py
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
```

the source_reader.py uses config.py when extract data from source data (jsonl)
```config.py
from pyspark.sql import types as T

schema_config = T.StructType([
    T.StructField("type", T.StringType(), True),
    T.StructField("width", T.DoubleType(), True),
    T.StructField("height", T.DoubleType(), True),
    T.StructField("base", T.DoubleType(), True),
    T.StructField("radius", T.DoubleType(), True)
])
```


# problem 2: the validate task should only label valid_data  meeting the schema that are matching those 3 shapes with right key, type,and value, rest of records should be labelled as `invalid`