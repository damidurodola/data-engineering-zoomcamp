### Question 1: Install Spark and PySpark
```
4.1.1
```

### Question 2: Yellow November 2025
Read the November 2025 Yellow into a Spark Dataframe.

Repartition the Dataframe to 4 partitions and save it to parquet.

What is the average size of the Parquet (ending with .parquet extension) Files that were created (in MB)? Select the answer which most closely matches.
```
25MB
```

### Question 3: Count records
How many taxi trips were there on the 15th of November?
- 167188
```
df_yellow.withColumn('pickup_date', F.to_date(df_yellow.tpep_pickup_datetime)) \
            .filter("pickup_date = '2025-11-15'") \
            .count()
```


### Question 4: Longest trip
What is the lenght of the longest trip in the dataset in hours?
- 90.6
```
df_with_duration = df_yellow.withColumn(
    "trip_hours",
    (F.unix_timestamp("tpep_dropoff_datetime") - F.unix_timestamp("tpep_pickup_datetime")) / 3600
).agg(F.max("trip_hours")) \
.show()
```

### Question 5: User Interface
Spark's User Interface which shows the application's dashboard runs on which local port?
```
4040
```

### Question 6: Least frequent pickup location zone
Using the zone lookup data and the Yellow November 2025 data, what is the name of the LEAST frequent pickup location Zone?
- Governor's Island/Ellis Island/Liberty Island
- Arden Heights
```
df_yellow.join(df_zones, df_yellow.PULocationID == df_zones.LocationID, 'left') \
    .groupBy("Zone") \
    .agg(F.count("*").alias("count")) \
    .orderBy("count") \
    .show()
```
