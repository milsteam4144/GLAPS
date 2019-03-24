import tensorflow as tf
from keras.models import load_model
import os
import numpy as np
import pandas as pd

path = os.path.abspath("model_4.h5")
model = load_model(path)

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
