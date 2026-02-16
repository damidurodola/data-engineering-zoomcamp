Analytics Engineering

This folder captures the core ideas behind analytics engineering, the bridge between data infrastructure and business-facing analytics.

Data Domain Trends

- Massively parallel processing databases unlock warehouse-scale compute.
- Pipelines-as-a-service tools reduce the need for bespoke orchestration code.
- SQL-first tooling keeps transformations accessible to analysts and engineers.
- Version control enables collaboration, reviews, and reproducibility.
- Self-service analytics platforms empower business teams.
- Data governance ensures quality, lineage, and compliance.

Roles in a Modern Data Team

- Data Engineer: builds and maintains ingestion, storage, and compute platforms.
- Analytics Engineer: applies software engineering practices to analytics code so analysts can ship faster with confidence.
- Data Analyst: leverages curated data to answer business questions and guide decisions.

Tooling Stack

- Data loading: batch or streaming ingestion services.
- Data storage: cloud warehouses such as Snowflake, BigQuery, or Redshift.
- Data modeling: transformation frameworks like dbt or Dataform.
- Data presentation: BI tools including Looker, Mode, Tableau, or Looker Studio.

Analytics engineers typically own the modeling and presentation layers, partnering closely with both engineers and analysts.

ETL vs. ELT

- ETL (Extract, Transform, Load) transforms data before it lands in the warehouse.
- ELT (Extract, Load, Transform) loads raw data first, leaving transformations to warehouse-native tools. Modern cloud warehouses favor ELT because compute is elastic and transformations are easier to version and monitor.

Kimball Dimensional Modeling

- Objective: deliver understandable data to business users and ensure fast query performance.
- Approach: prioritize ease of use over strict third-normal-form schemas by organizing data into star schemas.
- Fact tables capture measurable business processes (verbs) such as trips, sales, or subscriptions.
- Dimension tables describe business entities (nouns) such as customers, drivers, or locations.

dbt Overview

- dbt is a transformation workflow that lets teams write modular SQL models while following software engineering best practices (version control, tests, documentation, CI).
- Typical flow: data sources -> loaders -> warehouse (raw) -> dbt transforms -> BI tools and downstream consumers.
- Each dbt model is a single SELECT statement; dbt handles materialization (views, tables) and dependencies.
- dbt Core is the open-source CLI; dbt Cloud is the managed SaaS experience with a hosted IDE, scheduler, and metadata.

Loading Yellow Taxi Data

1. Run `python load_taxi_data.py` from this directory to download the source CSV files and upload them to the designated GCP bucket.
2. Create an external BigQuery table that references the GCS URIs:

```
-- Create an external table over the staged CSV files.
CREATE OR REPLACE EXTERNAL TABLE `majestic-option-485903-m2.zoomcamp.external_yellow_2019-2020_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://bigquery-zoomcamp-dami-demo/yellow_tripdata_*.csv.gz']
);
```

Next Steps

- Create a dbt Cloud account (or use dbt Core locally) and connect it to the warehouse.
- Complete the workspace setup checklist in `load_taxi_data.py` comments to ensure credentials, datasets, and schedules are in place.

