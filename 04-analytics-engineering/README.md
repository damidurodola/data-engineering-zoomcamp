Analytics Engineering

Data Domain Developments

- Massively Paralllel Processing DBs
- Data pipelines as a service
- SQL-first
- Version control systems
- Self sevice analytics
- Data Governance

Role sin a Data Team
- Datea Eninger- prepares and maintain the infrastructure the data team needs.
- Analytics Engineer -Introduces the good software engineering practices to help the efforts of data analysts and data scientists.
- Data Analyst - USe datat to answer questions and solve problems.

Tools
-Data loading
- Data storing: cloud data warehouses like snowflakes, bigquery, redshift
-Data modelling: Tools like dbt or Dataform
- Data presentation : BI tools like google data studio, Looker, Mode or Tableau

Analytics  engineer work with the last two tools

ETL vs ELT

Kimballs's Dimensional Modelling
Objective
- deliver understandable data to business users
- deliver fast uwery performance

Approach
priortize understandable data over non 3NF normalized DBS

StarSchema

Facts tables
- Measure ment, facts and corresponds to a business process (verbs) e.g

Dimensions tables
- relates to a business entity (nouns) e.d sales

DBT
A transformation workfloe that uses SQL tp deploy analytocs code follwing software enginering best practices.

data sources ---- data loaders ---data warehouse ---------- BI Tools, other data consumers
                                  raw data-dbt-transformed

Each dbt model is:
- a sql file, select statement(no DDL or DML)

How to use dbt?
dbt Core: opensource project allows data transformation

dbt Cloud: SaaS application to develop and manage dbt projects

How to Load Data
- Run the load_taxi_data.py to download from source and upload to a GCP Bucket.

```
-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `majestic-option-485903-m2.zoomcamp.external_yellow_2019-2020_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://bigquery-zoomcamp-dami-demo/yellow_tripdata_*.csv.gz']
);
```

