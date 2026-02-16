-- Creating external table referring to gcs path- yellow
CREATE OR REPLACE EXTERNAL TABLE `majestic-option-485903-m2.zoomcamp.external_yellow_2019_2020_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://bigquery-zoomcamp-dami-demo/yellow_tripdata_*.csv.gz']
);

-- Check yellow trip data
-- SELECT * FROM majestic-option-485903-m2.zoomcamp.external_yellow_tripdata limit 10;
SELECT COUNT(*) FROM majestic-option-485903-m2.zoomcamp.external_yellow_2019_2020_tripdata;

-- Creating external table referring to gcs path- green
CREATE OR REPLACE EXTERNAL TABLE `majestic-option-485903-m2.zoomcamp.external_green_2019_2020_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://bigquery-zoomcamp-dami-demo/green_tripdata_*.csv.gz']
);



-- Check green trip data
-- SELECT * FROM majestic-option-485903-m2.zoomcamp.external_green_tripdata limit 10;
SELECT COUNT(*) FROM majestic-option-485903-m2.zoomcamp.external_green_2019_2020_tripdata;

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE majestic-option-485903-m2.zoomcamp.yellow_2019_2020_tripdata AS
SELECT * FROM majestic-option-485903-m2.zoomcamp.external_yellow_2019_2020_tripdata;

-- Create a non partitioned table from external table - green
CREATE OR REPLACE TABLE majestic-option-485903-m2.zoomcamp.green_2019_2020_tripdata AS
SELECT * FROM majestic-option-485903-m2.zoomcamp.external_green_2019_2020_tripdata;

-- Get count of records in yellow trip data
SELECT COUNT(*) FROM majestic-option-485903-m2.zoomcamp.green_2019_2020_tripdata;

