## Data Processing Modes
- Batch processing handles finite datasets on a schedule (hourly, daily, weekly).
- Streaming processing handles unbounded data with low-latency requirements.

## Batch Processing Quick Facts
- Jobs are usually orchestrated with tools such as Airflow.
- Common execution engines: SQL, Spark, Flink, custom Python scripts or dbt models.
- Typical pipeline: data lake ➜ Python preprocessing ➜ SQL/dbt transforms ➜ Spark jobs ➜ downstream Python/ML tasks.

### Advantages
- Easier operational management and retries.
- Scaling is straightforward because workloads are bounded.

### Disadvantages
- Inherent delay between data arrival and availability (latency window equals batch schedule).

## Apache Spark Overview
- Distributed data processing engine written in Java/Scala with Python (PySpark) bindings.
- Excels when data already resides in a lake such as S3 or GCS.
- Example pattern: lake storage ➜ Spark SQL transforms ➜ write back to lake.

### Related SQL-on-Lake Engines
- Hive, Presto, and Athena can execute SQL directly on data lake files before or alongside Spark workloads.

### End-to-End ML Example
Raw data ➜ lake landing zone ➜ Athena SQL curates training sets ➜ Spark applies heavy transforms or ML feature engineering ➜ Python trains models ➜ artifacts returned to the lake.


