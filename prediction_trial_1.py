import tensorflow as tf
from keras.models import load_model
import os
import numpy as np

path = os.path.abspath("model_1.h5")
model = load_model(path)

"""
with all data used line 804 as it is not in training nor test data used
"""
input_data = [55,62583,50935,783,32381,3121,29629,115149,32770,62591,40.6,45977,3142]
input_data = tf.keras.utils.normalize(input_data, axis = -1, order = 2)
input_data = np.array(input_data)
prediction = model.predict(input_data)

print("Prediction w/ all attributes =",prediction[0][0], "True Value= 158500")

"""
only with state code
"""
input_data = [55,0,0,0,0,0,0,0,0,0,0,0,0]
input_data = tf.keras.utils.normalize(input_data, axis = -1, order = 2)
input_data = np.array(input_data)
prediction = model.predict(input_data)

print("Prediction w/ just state code =",prediction[0][0], "True Value= 158500")
