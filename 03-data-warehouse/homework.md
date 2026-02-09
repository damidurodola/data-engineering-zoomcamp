## BigQuery

### Counting Records
What is count of records for the 2024 Yellow Taxi Data?
- 20,332,093

```
SELECT COUNT(*) FROM majestic-option-485903-m2.zoomcamp.yellow_tripdata_non_partitioned;
```

### Data read estimation
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
```
SELECT DISTINCT COUNT(PULocationID) FROM majestic-option-485903-m2.zoomcamp.yellow_tripdata_non_partitioned; # Materialized Table

SELECT DISTINCT COUNT(PULocationID) FROM majestic-option-485903-m2.zoomcamp.external_yellow_tripdata; # External table
```

What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?
- 0 MB for the External Table and 155.12 MB for the Materialized Table

### Understanding columnar storage
Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table.
```
SELECT PULocationID FROM majestic-option-485903-m2.zoomcamp.yellow_tripdata_non_partitioned;
SELECT PULocationID, DOLocationID FROM majestic-option-485903-m2.zoomcamp.yellow_tripdata_non_partitioned;
```

Why are the estimated number of Bytes different?
- BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.

### Counting zero fare trips
How many records have a fare_amount of 0?
```
SELECT COUNT(*) FROM majestic-option-485903-m2.zoomcamp.yellow_tripdata_non_partitioned WHERE fare_amount = 0.0;
```
- 8,333

### Partitioning and Clustering
What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)
- Partition by tpep_dropoff_datetime and Cluster on VendorID

### Partition Benefits
Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive)

```
-- Impact of partition and clustering
-- Scanning 310.24 MB of data
SELECT DISTINCT(VendorID)
FROM majestic-option-485903-m2.zoomcamp.yellow_tripdata_non_partitioned
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';

-- Scanning ~ 26.84 MB of DATA
SELECT DISTINCT(VendorID)
FROM majestic-option-485903-m2.zoomcamp.yellow_tripdata_partitioned_clustered
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';
```

Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values?

- 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table

### External table storage
Where is the data stored in the External Table you created?
- GCP Bucket

### Clustering best practices
It is best practice in Big query to always cluster your data:
- False

### Understanding table scans
No Points: Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read?
-- It estimate 130.79 KB when run but actual bytes processed in 0B.

Why?
BigQuery returned a cached result from the previous query.

