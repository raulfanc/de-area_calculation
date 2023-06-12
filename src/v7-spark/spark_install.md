# Linux os Spark install

- log into gcp vm
- create a folder for `spark` 
```bash
mkdir spark /
cd spark
```

---

## install Java

1. install java
```bash
wget https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz
```

2. unzip java
```bash
tar xzfv openjdk-11.0.2_linux-x64_bin.tar.gz
```

3. `rm` the zip file

4. define `JAVA_HOME` and add it to `PATH`:

```shell
export JAVA_HOME="${HOME}/spark/jdk-11.0.2"
export PATH="${JAVA_HOME}/bin:${PATH}"
```

5. check that it works:

```shell
java --version
```

---

## install Spark

1. Download Spark. Use 3.3.2 version:

```shell
wget https://dlcdn.apache.org/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz

```

2. Unpack:

```shell
tar xzfv spark-3.3.2-bin-hadoop3.tgz
```

3. Remove the archive:

```shell
rm spark-3.3.2-bin-hadoop3.tgz
```

4. Add it to `PATH`:

```shell
export SPARK_HOME="${HOME}/spark/spark-3.3.2-bin-hadoop3"
export PATH="${SPARK_HOME}/bin:${PATH}"
```

### [](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_5_batch_processing/setup/linux.md#testing-spark)Testing Spark

1. Execute 
```bash
spark-shell
```

2. and run the following:

```scala
val data = 1 to 10000
val distData = sc.parallelize(data)
distData.filter(_ < 10).collect()
```

3. exit the `scala` shell and add export into `.bashrc`
```bash
cd ~
nano .bashrc
```

```nano
export JAVA_HOME="${HOME}/spark/jdk-11.0.2"
export PATH="${JAVA_HOME}/bin:${PATH}"

export SPARK_HOME="${HOME}/spark/spark-3.3.2-bin-hadoop3"
export PATH="${SPARK_HOME}/bin:${PATH}"
```

---
## install pyspark

```bash
cd ${SPARK_HOME}/python/lib/
```
check the file version


6.1 To run PySpark, we first need to add it to `PYTHONPATH`:

```shell
export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"
```

Make sure that the version under `${SPARK_HOME}/python/lib/` matches the filename of py4j or you will encounter `ModuleNotFoundError: No module named 'py4j'` while executing `import pyspark`.

For example, if the file under `${SPARK_HOME}/python/lib/` is `py4j-0.10.9.3-src.zip`, then the `export PYTHONPATH` statement above should be changed to

```shell
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"
```

---

6.2 port forwarding (listen to remote port), set up ssh chanel from **local terminal**

- update **vm ip** (gcp vm restarts has new ip)
```bash
nano ~/.ssh/config
```

- **jupyter notebook**
```bash
ssh -i ~/.ssh/gcp -L 8888:localhost:8888 rex@de-learning
```

- switch the env and start `jupyter notebook`
```bash
jupyter notebook .
```

- **spark**
```bash
ssh -i ~/.ssh/gcp -L 4040:localhost:4040 rex@de-learning
```

http://de-learning.australia-southeast1-b.c.de-learning-20190409.internal:4040


- **prefect**
```bash
ssh -i ~/.ssh/gcp -L 4200:localhost:4200 rex@de-learning
```

- switch to the env and start `prefect server`
```bash
prefect orion start```
```

---

6.3. run spark job
```python
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('plexure') \
    .getOrCreate()

    # Read JSON lines file into a DataFrame
    df = spark.read.option("multiline", "true").json('dummy_data.jsonl')

    # Convert DataFrame to list of dictionaries
    shapes_data = [row.asDict() for row in df.collect()]

    # Stop the SparkSession
    spark.stop()

    return shapes_data
```



