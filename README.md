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