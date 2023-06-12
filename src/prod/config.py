"""
A centralized place to manage these settings
"""

# Configure the "FLOW PARAMETERS" below===============
flow_param_config = {
    "input_path": 'dummy_data.jsonl',
    "parquet_path": 'bronze/',
    "silver_valid_path": 'silver/valid/',
    "silver_invalid_path": 'silver/invalid/',
    "invalid_rate": 5
}


# Configure the "SCHEMA" below========================
# - if add more shapes, can be defined here
from pyspark.sql import types as T

schema_config = T.StructType([
    T.StructField("type", T.StringType(), True),
    T.StructField("width", T.DoubleType(), True),
    T.StructField("height", T.DoubleType(), True),
    T.StructField("base", T.DoubleType(), True),
    T.StructField("radius", T.DoubleType(), True)
])

# ==================================================
