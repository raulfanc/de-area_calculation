# guide to install spark 3.2.1 for macos

1. install java
```bash
xcode-select –install
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
brew install java
```

2. Add the following environment variables to your .bash_profile or .zshrc:

```bash
export JAVA_HOME=/usr/local/Cellar/openjdk@11/11.0.12
export PATH="$JAVA_HOME/bin/:$PATH"
```

3. Make sure Java was installed to /usr/local/Cellar/openjdk@11/11.0.12: Open Finder > Press Cmd+Shift+G > paste "/usr/local/Cellar/openjdk@11/11.0.12". If you can't find it, then change the path location to appropriate path on your machine. You can also run brew info java to check where java was installed on your machine.

4. Install Apache Spark

4.1. install scala
```bash
brew install scala@2.11
```

4.2. install spark
```bash
brew install apache-spark
```

4.3. Add the following environment variables to your `.bash_profile` or `.zshrc`. Replace the path to `SPARK_HOME` to the path on your own host. Run `brew info apache-spark` to get this.

```bash
export SPARK_HOME=/usr/local/Cellar/apache-spark/3.2.1/libexec
export PATH="$SPARK_HOME/bin/:$PATH"
```

5. Testing Spark
Execute `spark-shell` and run the following in scala:
```
val data = 1 to 10000
val distData = sc.parallelize(data)
distData.filter(_ < 10).collect()
```

6. pyspark
6.1. To run PySpark, we first need to add it to `PYTHONPATH`:
```bash
export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9-src.zip:$PYTHONPATH"
```
Make sure that the version under `${SPARK_HOME}/python/lib/` matches the filename of py4j or you will encounter `ModuleNotFoundError: No module named 'py4j'` while executing `import pyspark`.

For example, if the file under `${SPARK_HOME}/python/lib/` is `py4j-0.10.9.3-src.zip`, then the `export PYTHONPATH` statement above should be changed to
```shell
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.3-src.zip:$PYTHONPATH"
```

6.2. run spark job
```python
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()

    # Read JSON lines file into a DataFrame
    df = spark.read.json('dummy_data.jsonl')

    # Convert DataFrame to list of dictionaries
    shapes_data = [row.asDict() for row in df.collect()]

    # Stop the SparkSession
    spark.stop()

    return shapes_data
```



