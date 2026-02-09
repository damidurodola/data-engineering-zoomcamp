# Data Warehouse

## OLAP vs OLTP
OLTP - Online Transaction Processing
Used for day‑to‑day operational systems.
- Optimized for fast inserts, updates, deletes
- Supports transactions and rollback
- Highly normalized schema (3NF)
- Small, frequent operations
Examples: banking systems, e‑commerce checkout, inventory systems

OLAP - Online Analytical Processing
Used for analytics, reporting, dashboards.
- Optimized for large scans and aggregations
- Data is denormalized for speed
- Refreshes periodically (batch or streaming)
- Supports historical analysis
Examples: dashboards, BI tools, forecasting, trend analysis

## Data Warehouse
Data Warehouse is an OLAP system designed for reporting and data analytics.


## BigQuery
BigQuery is a serverless, fully-managed cloud data warehouse and a Software as a Service platform (SaaS) which is designed for  scalability and high-availability.

Key capabilities are:
- Built‑in machine learning (BQML)
- Geospatial analytics
- Business intelligence integrations
- Massive parallel processing (MPP)

### BigQuery Architecture
BigQuery separates storage and compute:

#### Storage Layer — Colossus
- Distributed, replicated, columnar storage
- Cheap, durable, and scalable
- Stores data in compressed columnar format

#### Compute Layer — Dremel
- Executes SQL queries using a tree‑based execution engine.
- Massively parallel.
- Scans only the columns needed.

#### Network Layer — Jupiter.
- Google’s high‑speed datacenter network.
- Up to 1 TB/s bandwidth between compute and storage.
- Enables separation of compute and storage without performance loss.

### Partitioning in BigQuery
Partitioning splits a table into smaller segments.
It is best to partition by:
- DATE/TIMESTAMP column or
- Ingestion time (_PARTITIONTIME).

partition types:
- Daily (most common).
- Hourly (for high-volume streaming).
- Monthly or Yearly.
Max 4000 partitions per table.

Benefits:
- Reduces scanned bytes.
- Improves performance.
- Allows partition pruning.
- Predictable cost.


### Clustering in BigQuery
Clustering organizes data within each partition based on one or more columns.
#### Benefits:
- Faster filtering and aggregation
- Better pruning of data blocks
- Works well with high‑cardinality columns (e.g., user_id, timestamps)

#### When clustering helps
- Table is large (> 1 GB)
- Queries frequently filter on the cluster keys

#### When clustering does NOT help
- Table is small (< 1 GB)
- Columns have low cardinality (e.g., Y/N flags)
- Query patterns don’t align with cluster keys

#### Automatic Clustering
BigQuery automatically re‑clusters data as new rows arrive.

### Best Pratices in BigQuery
- To reduce cost
  - Avoid SELECT *: always select a specific column because data is stored in columns.
  - Preview query cost before running.
  - Partition and cluster large tables.
  - Use streaming inserts sparingly (they cost more).
  - Materialize intermediate results for complex pipelines.

- Query Performance
  - Always filter on partitioned columns.
  - Denormalize data.
  - Reduce data before using a JOIN.
  - Avoid oversharding tables.
  - Order large tables bydecreasing row sizes for better distribution.

