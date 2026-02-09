-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `majestic-option-485903-m2.zoomcamp.external_yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://bigquery-zoomcamp-dami-demo/*.parquet']
);

-- Check yellow trip data
-- SELECT * FROM majestic-option-485903-m2.zoomcamp.external_yellow_tripdata limit 10;
SELECT COUNT(*) FROM majestic-option-485903-m2.zoomcamp.external_yellow_tripdata;
-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE majestic-option-485903-m2.zoomcamp.yellow_tripdata_non_partitioned AS
SELECT * FROM majestic-option-485903-m2.zoomcamp.external_yellow_tripdata;

-- Get count of records in yellow trip data
SELECT COUNT(*) FROM majestic-option-485903-m2.zoomcamp.yellow_tripdata_non_partitioned;

-- Count Distinct number of PULocationIDS
SELECT PULocationID FROM majestic-option-485903-m2.zoomcamp.yellow_tripdata_non_partitioned;
SELECT PULocationID, DOLocationID FROM majestic-option-485903-m2.zoomcamp.yellow_tripdata_non_partitioned; #Table
-- SELECT DISTINCT COUNT(PULocationID) FROM majestic-option-485903-m2.zoomcamp.external_yellow_tripdata; # External table

SELECT COUNT(*) FROM majestic-option-485903-m2.zoomcamp.yellow_tripdata_non_partitioned WHERE fare_amount = 0.0;

-- Creating a partition and cluster table
CREATE OR REPLACE TABLE majestic-option-485903-m2.zoomcamp.yellow_tripdata_partitioned_clustered
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM majestic-option-485903-m2.zoomcamp.external_yellow_tripdata;

-- Impact of partition and clustering
-- Scanning 310.24 MB of data
SELECT DISTINCT(VendorID)
FROM majestic-option-485903-m2.zoomcamp.yellow_tripdata_non_partitioned
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';

-- Scanning ~ 26.84 MB of DATA
SELECT DISTINCT(VendorID)
FROM majestic-option-485903-m2.zoomcamp.yellow_tripdata_partitioned_clustered
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';

-- table scans This script will process 130.79 KB when run but actual bytes processed in 0B.
SELECT COUNT(*)
FROM majestic-option-485903-m2.zoomcamp.yellow_tripdata_non_partitioned;

