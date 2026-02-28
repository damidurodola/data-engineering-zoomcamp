/* @bruin

name: staging.trips
type: bq.sql
depends:
  - ingestion.trips
  - ingestion.payment_lookup
materialization:
  type: table

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
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY t.pickup_datetime, t.dropoff_datetime,
         t.pickup_location_id, t.dropoff_location_id,
         SAFE_CAST(t.fare_amount AS NUMERIC)
    ORDER BY t.pickup_datetime
) = 1

