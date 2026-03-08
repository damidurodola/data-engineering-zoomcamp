Types of Processing Data
- Batch
- Streaming
What is Batch Processing?
 -
Could be hourly,daily, weekly,
 Technologies
SQL, Spark, Flink, Python Scripts. Airflow is used to execute the jobs.

Lake ---> Python ----> SQL(dbt)----> Spark----> Python

Advatanges
- Easy to manage.
- Retry.
- Easier to scale.

Disadvantage
- Delay

Apache Spark (data processing engine)
It is written in JAVA and SCALA with Python wrappers.

When to use Spark?
When data is in a DataLake

DataLake (S3/GCS) ----> Spark(Sql) ------> DataLake

Hive Presto/Athena can be used to execute SQL in datalakes

Raw data ---> Lake ----> SQL athena ---> spark----> Python (train ML)
                                          ---Spark(Apply ML)
                                          ----Lake
