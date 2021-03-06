import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import keras
from keras.models import Sequential
from keras.layers import *

training_data_df = pd.read_csv("train_data_scaled.csv")

X = training_data_df.drop('medianHomeVal', axis=1).values
Y = training_data_df[['medianHomeVal']].values

# Define the mode
model = Sequential()

model.add(Dense(200, input_dim = 14, activation = 'relu'))
model.add(Dense(30, activation = 'relu'))
model.add(Dense(400, activation = 'relu'))
model.add(Dense(10, activation = 'relu'))
model.add(Dense(250, activation = 'relu'))
model.add(Dense(1, activation = 'linear'))

model.compile(loss = 'mean_squared_error', optimizer = 'adam')

# Create a TensorBoard logger
logger = keras.callbacks.TensorBoard(log_dir="logs", write_graph=True,
                                     histogram_freq=0)

# Train the model (X&Y = data and data targets epochs is num of iterations
# shuffle is to shuffle data verbose  is to visualize what is happening

model.fit(X,Y, epochs = 400, shuffle = True, verbose = 2, callbacks = [logger])

# Load the separate test data set
test_data_df = pd.read_csv("test_data_scaled.csv")

X_test = test_data_df.drop('medianHomeVal', axis=1).values
Y_test = test_data_df[['medianHomeVal']].values

#Evaluates Model
test_error_rate = model.evaluate(X_test, Y_test, verbose = 0)
print("The mean squared error (MSE) for the test data set is: {}".format(test_error_rate))

# Load the data we make to use to make a prediction (manually scaled)
X = pd.read_csv("prediction_data.csv").values
                               
# Make a prediction with the neural network
prediction = model.predict(X)

# Grab just the first element of the first prediction (since that's the only have one)
prediction = prediction[0][0]

# Re-scale the data from the 0-to-1 range back to dollars
# These constants are from when the data was originally scaled down to the 0-to-1 range
# Note: medHomeVal values were scaled by multiplying by 0.0000001018 and adding -0.006588
prediction = prediction + 0.109171
prediction = prediction / 0.0000015184

print("Median Home Value Prediction - ${}".format(prediction))
print("True Value = $158500")

model.save('model_5.h5')
