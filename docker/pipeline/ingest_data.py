#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import click

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

# df = pd.read_csv(
#     url,
#     # nrows=100,
#     dtype=dtype,
#     parse_dates=parse_dates
# )


# print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))

# df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')

@click.command()
@click.option('--pg_user', default='root', help='PostgreSQL user')
@click.option('--pg_pass', default='root', help='PostgreSQL password')
@click.option('--pg_host', default='localhost', help='PostgreSQL host')
@click.option('--pg_port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg_db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--table_name', default='yellow_taxi_data', help='Target table name')
@click.option('--year', default=2021, type=int, help='Year of the data to ingest')
@click.option('--month', default=1, type=int, help='Month of the data to ingest')
@click.option('--chunksize', default=100000, type=int, help='Number of rows per chunk to ingest')

def run(pg_user, pg_pass, pg_host, pg_port, pg_db, table_name, year, month, chunksize):
    # year=y
    # month=1
    # pg_user= 'root'
    # pg_pass = 'root'
    # pg_host= 'localhost'
    # pg_port= 5432
    # pg_db= 'ny_taxi'
    # chunksize = 100000
    # table_name = 'yellow_taxi_data'

    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url = f"{prefix}yellow_tripdata_{year:04d}-{month:02d}.csv.gz"

#     df = pd.read_csv(
#     url,
#     # nrows=100,
#     dtype=dtype,
#     parse_dates=parse_dates

# )

    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        iterator=True,
        chunksize=chunksize,
        parse_dates=parse_dates
    )

    first = True

    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(0).to_sql(name=table_name, con=engine, if_exists='replace')
            first = False

        df_chunk.to_sql(name=table_name, con=engine, if_exists='append')
        # print(len(df_chunk))

if __name__ == "__main__":
    run()

