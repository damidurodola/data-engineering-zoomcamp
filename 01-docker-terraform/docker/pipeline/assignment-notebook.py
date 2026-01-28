#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[4]:


get_ipython().system('wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet')


# In[5]:


get_ipython().system('wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv')


# In[27]:


dtype = {
    "RatecodeID": "Int64",
    "passenger_count": "Int64",
    "payment_type": "float64",
    "trip_type": "Int64",

}


# In[64]:


df = pd.read_parquet("green_tripdata_2025-11.parquet")


# In[48]:


get_ipython().system('uv add fastparquet')


# In[49]:


from fastparquet import ParquetFile

pf = ParquetFile('green_tripdata_2025-11.parquet')




# In[51]:


pf.head(nrows=4)


# In[ ]:





# In[36]:


# df = df.astype({"RatecodeID": "Int64",
#     "passenger_count": "Int64",
#     "payment_type": "Int64",
#     "trip_type": "Int64"})


# In[65]:


df.head()


# In[42]:


df.shape


# In[ ]:





# In[9]:


df.dtypes


# In[38]:


df['payment_type'].value_counts()


# In[20]:


taxi_df = pd.read_csv("taxi_zone_lookup.csv.1")


# In[21]:


taxi_df.dtypes


# In[22]:


taxi_df.head()


# In[58]:


taxi_df.shape


# In[39]:


from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')


# In[40]:


print(pd.io.sql.get_schema(df, name='green_tripdata_2025-11', con=engine))


# In[62]:


df.to_sql(name='green_tripdata_2025_11', con=engine, if_exists='replace')


# In[61]:


from tqdm.auto import tqdm
first_chunk = next(pf.iter_row_groups())

first_chunk.head(0).to_sql(
    name="green_tripdata_2025_11",
    con=engine,
    if_exists="replace"
)

print("Table created")

first_chunk.to_sql(
    name="green_tripdata_2025_11",
    con=engine,
    if_exists="append"
)

print("Inserted first chunk:", len(first_chunk))

# for df_chunk in tqdm(df_iter):
for df_chunk in tqdm(pf.iter_row_groups()):
    df_chunk.to_sql(
        name="green_tripdata_2025_11",
        con=engine,
        if_exists="append"
    )
    print("Inserted chunk:", len(df_chunk))


# In[60]:


taxi_df.to_sql(name='taxi_zone_lookup', con=engine, if_exists='replace')


# In[67]:


uv run jupyter nbconvert --to=script assignment-notebook.ipynb

