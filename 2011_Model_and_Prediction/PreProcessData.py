import os
from sqlalchemy import create_engine
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

path = os.path.abspath("MinorLeague.db")
engine = create_engine("sqlite:///"+path, echo = False)#Set to false to git rid of log
#Link a session to the engine and initialize it
conn = engine.connect()

df = pd.read_sql_table('all_3_Data', conn)
df = df[:800]
df = df.drop(['CountyCode'], axis = 1)
df = df.drop(['Year'], axis = 1)
df = df.drop(['StateAndCounty'], axis = 1)
df['StateCode'] = pd.to_numeric(df['StateCode'],errors='coerce').fillna(0)

#randomly takes 70% of the DB dataset and places it in train
train_df = df.sample(frac = 0.7, random_state=800)

#places remaining items in test db
test_df = df.drop(train_df.index)

# Data needs to be scaled to a small range like 0 to 1 for the neural
# network to work well.
scaler = MinMaxScaler(feature_range =(0,1))

# Scale both the training inputs and outputs
scaled_training = scaler.fit_transform(train_df)
scaled_testing = scaler.transform(test_df)


# Print out the adjustment that the scaler applied to the data num 2 is medHomeVal
i = 0
while i<15:
    print("Note: values were scaled by multiplying by {:.10f} and adding {:.6f}".format(scaler.scale_[i], scaler.min_[i]))
    i += 1
# Create new pandas DataFrame objects from the scaled data
scaled_train_df = pd.DataFrame(scaled_training, columns=train_df.columns.values)
scaled_test_df = pd.DataFrame(scaled_testing, columns=test_df.columns.values)

# Save scaled data dataframes to new CSV files
scaled_train_df.to_csv("train_data_scaled.csv", index=False)
scaled_test_df.to_csv("test_data_scaled.csv", index=False)
