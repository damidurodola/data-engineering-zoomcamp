/* @bruin

# Docs:
# - SQL assets: https://getbruin.com/docs/bruin/assets/sql
# - Materialization: https://getbruin.com/docs/bruin/assets/materialization
# - Quality checks: https://getbruin.com/docs/bruin/quality/available_checks

# TODO: Set the asset name (recommended: reports.trips_report).
name: reports.trips_report

# TODO: Set platform type.
# Docs: https://getbruin.com/docs/bruin/assets/sql
# suggested type: duckdb.sql
type: bq.sql

# TODO: Declare dependency on the staging asset(s) this report reads from.
depends:
  - staging.trips

# TODO: Choose materialization strategy.
# For reports, `time_interval` is a good choice to rebuild only the relevant time window.
# Important: Use the same `incremental_key` as staging (e.g., pickup_datetime) for consistency.
materialization:
  type: table

# TODO: Define report columns + primary key(s) at your chosen level of aggregation.
columns:
  - name: pickup_date
    type: date
    primary_key: true
    description: UTC calendar date of the trip pickup.
  - name: taxi_type
    type: string
    primary_key: true
    description: Taxi fleet category (yellow or green).
  - name: payment_type_name
    type: string
    primary_key: true
    description: Payment lookup label used for aggregation.
  - name: trips
    type: integer
    description: Total trips captured for the dimension grain.
  - name: total_distance_miles
    type: float
    description: Sum of trip_distance miles.
  - name: avg_distance_miles
    type: float
    description: Average trip_distance miles.
  - name: total_fare_amount
    type: float
    description: Sum of fare_amount in USD.
  - name: total_tip_amount
    type: float
    description: Sum of tip_amount in USD.
  - name: total_revenue_amount
    type: float
    description: Sum of total_amount in USD.

custom_checks:
  - name: row_count_greater_than_zero
    query: |
      WITH candidate_rows AS (
        SELECT
            t.pickup_datetime,
            t.dropoff_datetime,
            t.pickup_location_id,
            t.dropoff_location_id,
            t.fare_amount,
            t.taxi_type,
            p.payment_type_name
        FROM ingestion.trips t
        LEFT JOIN ingestion.payment_lookup p
            ON t.payment_type = p.payment_type_id
        WHERE t.pickup_datetime >= '{{ start_datetime }}'
          AND t.pickup_datetime < '{{ end_datetime }}'
      )
      SELECT CASE WHEN COUNT(*) > 0 THEN 1 ELSE 0 END FROM candidate_rows
    value: 1


@bruin */

WITH filtered AS (
    SELECT
        DATE(t.pickup_datetime) AS pickup_date,
        t.taxi_type,
        COALESCE(t.payment_type_name, 'unknown') AS payment_type_name,
        CASE WHEN t.fare_amount < 0 THEN NULL ELSE t.fare_amount END AS fare_amount,
    FROM staging.trips t
    WHERE t.pickup_datetime >= '{{ start_datetime }}'
      AND t.pickup_datetime < '{{ end_datetime }}'
), aggregated AS (
    SELECT
        pickup_date,
        taxi_type,
        payment_type_name,
        COUNT(*) AS trips,
        COALESCE(SUM(fare_amount), 0) AS total_fare_amount,
    FROM filtered
    GROUP BY pickup_date, taxi_type, payment_type_name
)

SELECT
    pickup_date,
    taxi_type,
    payment_type_name,
    trips,
    total_fare_amount,
FROM aggregated
ORDER BY pickup_date, taxi_type, payment_type_name
