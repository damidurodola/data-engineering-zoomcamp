from nbconvert import export

import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[*]").appName("test").getOrCreate()

print(f"Spark version: {spark.version}")

df = spark.range(10)
df.show()

spark.stop()


# export SPARK_HOME="${HOME}/Desktop/PHD/PERSONAL_CODE/Zoomcamp_data/06-batch-processing/spark-4.1.1-bin-hadoop3"
# export PATH="${SPARK_HOME}/bin:${PATH}"

export PYTHONPATH="${SPARK_HOME}/python:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9-src.zip:${PYTHONPATH}"
