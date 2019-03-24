import os
from sqlalchemy import create_engine
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

path = os.path.abspath("MinorLeague.db")
engine = create_engine("sqlite:///"+path, echo = False)#Set to false to git rid of log
#Link a session to the engine and initialize it
conn = engine.connect()

df = pd.read_sql_table('NC', conn)
#df = df[:800]
#df = df.drop(['CountyCode'], axis = 1)
df = df.drop(['StateCode'], axis = 1)
#df = df.drop(['StateAndCounty'], axis = 1)
df['CountyCode'] = pd.to_numeric(df['CountyCode'],errors='coerce').fillna(0)
"""
reshape data by county by year
"""
#randomly takes 70% of the DB dataset and places it in train
#train_df = df.sample(frac = 0.7).values
df = df.sort_values(by=['CountyCode'])
df = df.values
print(df.shape)

a = df.reshape(40, 7, 16)
print(a)
