import os
from sqlalchemy import create_engine
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import keras
from keras.models import Sequential
from keras.layers import *
from sklearn.externals import joblib



path = os.path.abspath("MinorLeague.db")
engine = create_engine("sqlite:///"+path, echo = False)#Set to false to git rid of log
#Link a session to the engine and initialize it
conn = engine.connect()

df = pd.read_sql_table('all_3_Data', conn)
df = df[4898:]
df = df.drop(['CountyCode'], axis = 1)
df = df.drop(['Year'], axis = 1)
df = df.drop(['State_Cty'], axis = 1)
df['StateCode'] = pd.to_numeric(df['StateCode'],errors='coerce').fillna(0)

#randomly takes 70% of the DB dataset and places it in train
train_df = df.sample(frac = 0.7)

#places remaining items in test db
test_df = df.drop(train_df.index)


#Break the data into data and targets
train_data = train_df.drop('medianHomeVal', axis=1).values
train_targets= train_df[['medianHomeVal']].values

test_data = test_df.drop('medianHomeVal', axis=1).values
test_targets = test_df[['medianHomeVal']].values

#Convert the output to a matrix
#train_targets = train_targets.reshape(-1,1)
#test_targets = test_targets.reshape(-1,1)


# Create two scalars- one for data and one for targets
sc_data = MinMaxScaler(feature_range =(0,1))
sc_targets = MinMaxScaler(feature_range =(0,1))

#Scale the data
train_data = sc_data.fit_transform(train_data)
test_data = sc_data.transform(test_data)

#Scale the targets
train_targets = sc_targets.fit_transform(train_targets)
test_targets = sc_targets.transform(test_targets)

#Save the scalers
joblib.dump(sc_data, "sc_data.save")
joblib.dump(sc_targets, "sc_targets.save")

'''
#Save the scaler
joblib.dump(scaler, "2017_scaler.save")

# Create new pandas DataFrame objects from the scaled data
scaled_train_df = pd.DataFrame(scaled_training, columns=train_df.columns.values)
scaled_test_df = pd.DataFrame(scaled_testing, columns=test_df.columns.values)


# Save scaled data dataframes to new CSV files
scaled_train_df.to_csv("train_data_scaled.csv", index=False)
scaled_test_df.to_csv("test_data_scaled.csv", index=False)
'''

# Define the model
model = Sequential()
model.add(Dense(200, input_dim=15, activation='relu'))
model.add(Dense(30, activation='relu'))
model.add(Dense(400, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(250, activation='relu'))
model.add(Dense(1, activation='linear'))

model.compile(loss='mean_squared_error', optimizer='adam')

# Create a TensorBoard logger
logger = keras.callbacks.TensorBoard(log_dir="logs", write_graph=True,
                                     histogram_freq=0)

# Train the model (X&Y = data and data targets epochs is num of iterations
# shuffle is to shuffle data verbose  is to visualize what is happening
model.fit(train_data, train_targets, epochs=400, shuffle=True, verbose=2, callbacks=[logger])


# Evaluates Model
test_error_rate = model.evaluate(test_data, test_targets, verbose=0)
print("The mean squared error (MSE) for the test data set is: {}".format(test_error_rate))


# Make a prediction with the neural network
prediction = model.predict(test_data[0].reshape(1,-1))

#Convert the values back to their pre-scaled form
actual_value = sc_targets.inverse_transform(test_targets)[0][0]
pred_value = sc_targets.inverse_transform(prediction)[0][0]


print('Actual Value: $', actual_value, 'Predicted Value: $', pred_value)

print('The difference is: $',abs(actual_value - pred_value))

model.save('model_2017.h5')





