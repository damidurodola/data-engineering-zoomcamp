"""@bruin

name: ingestion.trips
type: python
image: python:3.11
connection: gcp-default
columns:
  - name: vendor_id
    type: integer
    description: TLC vendor identifier supplied by the taxi fleet.
  - name: taxi_type
    type: string
    description: Taxi fleet type requested for the run (yellow or green).
  - name: pickup_datetime
    type: timestamp
    description: Timestamp when the trip began.
  - name: dropoff_datetime
    type: timestamp
    description: Timestamp when the trip ended.
  - name: passenger_count
    type: integer
    description: Number of passengers reported by the driver.
  - name: trip_distance
    type: float
    description: Trip distance in miles recorded by the meter.
  - name: rate_code_id
    type: integer
    description: TLC rate code identifier captured at pickup.
  - name: store_and_fwd_flag
    type: string
    description: Flag indicating if the record was stored and forwarded later.
  - name: pickup_location_id
    type: integer
    description: TLC taxi zone for the pickup location.
  - name: dropoff_location_id
    type: integer
    description: TLC taxi zone for the dropoff location.
  - name: payment_type
    type: integer
    description: Numeric payment key used to join with lookup tables.
  - name: fare_amount
    type: float
    description: Metered fare amount in USD.
  - name: extra
    type: float
    description: Miscellaneous surcharge total.
  - name: mta_tax
    type: float
    description: Mandatory MTA tax in USD.
  - name: tip_amount
    type: float
    description: Tip amount reported in USD.
  - name: tolls_amount
    type: float
    description: Tolls assessed during the trip.
  - name: improvement_surcharge
    type: float
    description: TLC improvement surcharge assessed per trip.
  - name: total_amount
    type: float
    description: Total amount billed to the rider including surcharges.
  - name: congestion_surcharge
    type: float
    description: Congestion surcharge amount applied within Manhattan.
  - name: airport_fee
    type: float
    description: Airport access fee for yellow taxis (0 when not applicable).
  - name: trip_type
    type: integer
    description: "Trip type code (green taxis only: 1=street hail, 2=dispatch)."
  - name: ehail_fee
    type: float
    description: Electronic hail fee reported by green taxis.
  - name: data_file_name
    type: string
    description: Source parquet file name for lineage tracking.
  - name: data_file_url
    type: string
    description: Fully qualified TLC CDN URL for the source file.
  - name: extracted_at
    type: timestamp
    description: UTC timestamp when this file was ingested.

@bruin"""

import io
import json
import logging
import os
from datetime import date, datetime, timedelta
from typing import Iterator, List, Tuple

import pandas as pd
import requests
from dateutil import parser as dateutil_parser
from dateutil.relativedelta import relativedelta
from google.api_core.exceptions import NotFound
from google.cloud import bigquery
from google.oauth2 import service_account


logger = logging.getLogger(__name__)

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"
SUPPORTED_TAXI_TYPES = {"yellow", "green"}

EXPECTED_COLUMNS = [
    "vendor_id",
    "taxi_type",
    "pickup_datetime",
    "dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "rate_code_id",
    "store_and_fwd_flag",
    "pickup_location_id",
    "dropoff_location_id",
    "payment_type",
    "fare_amount",
    "extra",
    "mta_tax",
    "tip_amount",
    "tolls_amount",
    "improvement_surcharge",
    "total_amount",
    "congestion_surcharge",
    "airport_fee",
    "trip_type",
    "ehail_fee",
    "data_file_name",
    "data_file_url",
    "extracted_at",
]

COLUMN_RENAMES_COMMON = {
    "VendorID": "vendor_id",
    "RatecodeID": "rate_code_id",
    "PULocationID": "pickup_location_id",
    "DOLocationID": "dropoff_location_id",
    "Store_and_fwd_flag": "store_and_fwd_flag",
    "store_and_fwd_flag": "store_and_fwd_flag",
    "Payment_type": "payment_type",
    "Trip_type": "trip_type",
    "Airport_fee": "airport_fee",
}

COLUMN_RENAMES_BY_TYPE = {
    "yellow": {
        "tpep_pickup_datetime": "pickup_datetime",
        "tpep_dropoff_datetime": "dropoff_datetime",
    },
    "green": {
        "lpep_pickup_datetime": "pickup_datetime",
        "lpep_dropoff_datetime": "dropoff_datetime",
    },
}


def main() -> None:
    """Fetch TLC trip data for the requested window and stream it into BigQuery."""

    start_dt, end_dt = _get_run_window()
    if start_dt >= end_dt:
        raise ValueError("BRUIN run window must have end > start")

    taxi_types = _load_taxi_types()
    extracted_at = datetime.utcnow()
    frames: List[pd.DataFrame] = []

    for taxi_type in taxi_types:
        for month_start in _iter_months(start_dt, end_dt):
            url = _build_url(taxi_type, month_start)
            logger.info("Fetching %s", url)
            try:
                raw_df = _download_parquet(url)
            except FileNotFoundError:
                logger.warning("No TLC file found at %s; skipping", url)
                continue
            except requests.HTTPError as exc:
                raise RuntimeError(f"HTTP error while downloading {url}") from exc
            except requests.RequestException as exc:
                raise RuntimeError(f"Network error while downloading {url}") from exc

            if raw_df.empty:
                logger.info("Source file %s contained 0 rows; skipping", url)
                continue

            frames.append(_normalize_dataframe(raw_df, taxi_type, url, extracted_at))

    if not frames:
        logger.info(
            "No NYC taxi data found for taxi_types=%s within %s -> %s",
            taxi_types,
            start_dt,
            end_dt,
        )
        return

    final_df = pd.concat(frames, ignore_index=True)
    _load_to_bigquery(final_df)


def _get_run_window() -> Tuple[datetime, datetime]:
    start_raw = os.environ.get("BRUIN_START_DATETIME") or os.environ.get("BRUIN_START_DATE")
    end_raw = os.environ.get("BRUIN_END_DATETIME") or os.environ.get("BRUIN_END_DATE")
    if not start_raw or not end_raw:
        raise ValueError("BRUIN start/end datetime variables are required for ingestion.trips")
    return _parse_datetime(start_raw), _parse_datetime(end_raw)


def _parse_datetime(value: str) -> datetime:
    try:
        if len(value) == 10 and value.count("-") == 2:
            return datetime.strptime(value, "%Y-%m-%d")
        return dateutil_parser.isoparse(value)
    except ValueError as exc:
        raise ValueError(f"Invalid datetime '{value}' supplied to ingestion.trips") from exc


def _load_taxi_types() -> List[str]:
    raw_vars = os.environ.get("BRUIN_VARS", "{}") or "{}"
    try:
        parsed = json.loads(raw_vars)
    except json.JSONDecodeError as exc:
        raise ValueError("BRUIN_VARS must contain valid JSON") from exc

    taxi_types = parsed.get("taxi_types", ["yellow"])
    if not isinstance(taxi_types, list):
        raise ValueError("taxi_types must be a list of strings")

    normalized: List[str] = []
    for entry in taxi_types or ["yellow"]:
        if not isinstance(entry, str):
            raise ValueError("Each taxi_types entry must be a string")
        cleaned = entry.strip().lower()
        if cleaned not in SUPPORTED_TAXI_TYPES:
            raise ValueError(
                f"Unsupported taxi type '{entry}'. Expected one of {sorted(SUPPORTED_TAXI_TYPES)}"
            )
        if cleaned not in normalized:
            normalized.append(cleaned)

    return normalized or ["yellow"]


def _iter_months(start: datetime, end: datetime) -> Iterator[date]:
    """Yield the first day of each month that overlaps the [start, end) window."""

    current = start.date().replace(day=1)
    inclusive_end = (end - timedelta(microseconds=1)).date()
    if inclusive_end < current:
        return
    terminal_month = inclusive_end.replace(day=1)

    while current <= terminal_month:
        yield current
        current = (current + relativedelta(months=1)).replace(day=1)


def _build_url(taxi_type: str, month_start: date) -> str:
    return f"{BASE_URL}/{taxi_type}_tripdata_{month_start.year}-{month_start.month:02d}.parquet"


def _download_parquet(url: str) -> pd.DataFrame:
    response = requests.get(url, timeout=120)
    if response.status_code == 404:
        raise FileNotFoundError(url)
    response.raise_for_status()
    return pd.read_parquet(io.BytesIO(response.content))


def _normalize_dataframe(
    df: pd.DataFrame, taxi_type: str, url: str, extracted_at: datetime
) -> pd.DataFrame:
    rename_map = {**COLUMN_RENAMES_COMMON, **COLUMN_RENAMES_BY_TYPE[taxi_type]}
    df = df.rename(columns=rename_map)

    missing_core = [col for col in ("pickup_datetime", "dropoff_datetime") if col not in df.columns]
    if missing_core:
        raise ValueError(f"Missing columns {missing_core} in source {url}")

    df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"], errors="coerce")
    df["dropoff_datetime"] = pd.to_datetime(df["dropoff_datetime"], errors="coerce")
    df["taxi_type"] = taxi_type
    df["data_file_name"] = url.split("/")[-1]
    df["data_file_url"] = url
    df["extracted_at"] = pd.Timestamp(extracted_at, tz="UTC")

    return df.reindex(columns=EXPECTED_COLUMNS)


def _load_to_bigquery(df: pd.DataFrame) -> None:
  dataset = os.environ.get("INGESTION_BIGQUERY_DATASET", "ingestion")
  table = os.environ.get("INGESTION_BIGQUERY_TABLE", "trips")
  location = os.environ.get("INGESTION_BIGQUERY_LOCATION")
  project = os.environ.get("INGESTION_BIGQUERY_PROJECT")
  client = _build_bigquery_client(project)
  project = project or client.project
  table_id = f"{project}.{dataset}.{table}"

  _ensure_destination(client, project, dataset, table, location)

  job_config = bigquery.LoadJobConfig(write_disposition=bigquery.WriteDisposition.WRITE_APPEND)
  logger.info("Loading %s rows into %s", len(df), table_id)
  job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
  job.result()
  logger.info("Finished loading %s", table_id)


def _ensure_destination(
  client: bigquery.Client, project: str, dataset: str, table: str, location: str | None
) -> None:
  dataset_id = f"{project}.{dataset}"
  dataset_ref = bigquery.Dataset(dataset_id)
  if location:
    dataset_ref.location = location
  try:
    client.get_dataset(dataset_ref)
  except NotFound:
    logger.info("Creating dataset %s", dataset_id)
    client.create_dataset(dataset_ref, exists_ok=True)

  table_id = f"{project}.{dataset}.{table}"
  table_ref = bigquery.Table(table_id, schema=_build_bq_schema())
  try:
    client.get_table(table_ref)
  except NotFound:
    logger.info("Creating table %s", table_id)
    client.create_table(table_ref, exists_ok=True)


def _build_bq_schema() -> List[bigquery.SchemaField]:
  type_mapping = {
    "integer": bigquery.SqlTypeNames.INT64,
    "float": bigquery.SqlTypeNames.FLOAT64,
    "timestamp": bigquery.SqlTypeNames.TIMESTAMP,
    "string": bigquery.SqlTypeNames.STRING,
  }
  schema = []
  for column in EXPECTED_COLUMNS:
    col_type = "string"
    if column in {
      "vendor_id",
      "passenger_count",
      "rate_code_id",
      "pickup_location_id",
      "dropoff_location_id",
      "payment_type",
      "trip_type",
    }:
      col_type = "integer"
    elif column in {
      "trip_distance",
      "fare_amount",
      "extra",
      "mta_tax",
      "tip_amount",
      "tolls_amount",
      "improvement_surcharge",
      "total_amount",
      "congestion_surcharge",
      "airport_fee",
      "ehail_fee",
    }:
      col_type = "float"
    elif column in {"pickup_datetime", "dropoff_datetime", "extracted_at"}:
      col_type = "timestamp"

    schema.append(bigquery.SchemaField(column, type_mapping[col_type], mode="NULLABLE"))

  return schema


def _build_bigquery_client(project: str | None) -> bigquery.Client:
  file_path = os.environ.get("INGESTION_BIGQUERY_SERVICE_ACCOUNT_FILE")
  json_blob = os.environ.get("INGESTION_BIGQUERY_SERVICE_ACCOUNT_JSON")

  if json_blob:
    try:
      info = json.loads(json_blob)
    except json.JSONDecodeError as exc:
      raise ValueError("INGESTION_BIGQUERY_SERVICE_ACCOUNT_JSON must contain valid JSON") from exc
    credentials = service_account.Credentials.from_service_account_info(info)
  elif file_path:
    credentials = service_account.Credentials.from_service_account_file(file_path)
  else:
    raise ValueError(
      "Set INGESTION_BIGQUERY_SERVICE_ACCOUNT_FILE or INGESTION_BIGQUERY_SERVICE_ACCOUNT_JSON"
    )

  scoped_credentials = credentials.with_scopes(["https://www.googleapis.com/auth/bigquery"])
  return bigquery.Client(project=project, credentials=scoped_credentials)


if __name__ == "__main__":
  main()





# export INGESTION_BIGQUERY_SERVICE_ACCOUNT_FILE="03-data-warehouse/gcs.json"
# export INGESTION_BIGQUERY_PROJECT="majestic-option-485903-m2"
# export INGESTION_BIGQUERY_DATASET="ingestion"
# export INGESTION_BIGQUERY_TABLE="trips"
# export INGESTION_BIGQUERY_LOCATION="us-central1"
# bruin run ./pipeline/assets/ingestion/trips.py --environment default --start-date 2022-01-01 --end-date 2022-03-01
