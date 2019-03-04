import os
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.ion()
from mpl_toolkits.mplot3d import Axes3D
import tensorflow as tf
import keras
from keras.models import Sequential, Model, Input
from keras.layers import Dense, Activation
#from keras.callbacks import TensorBoard

"""
Print versions of tensorflow and keras
"""
print('tensorflow_version:',tf.__version__)
print('keras_version:',keras.__version__)

"""
Gets data from DB
"""
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

#randomly takes 50% of the DB dataset and places it in train
train = df.sample(frac = 0.7, random_state=800)

#places remaining items in test db
test = df.drop(train.index)

"""
normalize train data
"""

"""
features
"""
train_targets = train['medianHomeVal']
train_data = train.drop(['medianHomeVal'], axis = 1)

train_data = tf.keras.utils.normalize(train_data, axis = -1, order = 2)
   
#makes data numpy arrays
train_data=np.array(train_data)
train_targets = np.array(train_targets)

#normalizes data from 0 - 1
print (train_data)

"""
Keras Model
"""
"""
#empty model
model = Sequential()
#uses sequential model
model.add(Dense(1,input_dim=5, kernel_initializer='normal',activation='relu'))

model.compile(loss='mse', optimizer='adam')
"""
#uses functional API model
inputs = Input(shape=(14,))
x = Dense(560,activation='relu')(inputs)
preds = Dense(1,activation='relu')(x)

model_2 = Model(inputs=inputs,outputs=preds)
#sgd=keras.optimezer.SGD()
model_2.compile(optimizer='adam', loss = 'mse', metrics=['mse'])

"""
Train Model
"""

#Train the model
hist = model_2.fit(train_data,train_targets,batch_size=1, epochs = 560)

#visualizing losses and accuracy
num_epochs = 560
train_losses=hist.history['loss']
xc=range(num_epochs)

plt.figure(1,figsize=(7,5))
plt.plot(xc,train_losses)
plt.xlabel('num of epochs')
plt.ylabel('loss')
plt.title('Train_loss')
plt.grid(True)
print(plt.style.available)
plt.style.use(['classic'])

"""
normalize test data
"""

test_targets = test['medianHomeVal']
test_data = test.drop(['medianHomeVal'], axis = 1)

test_data = tf.keras.utils.normalize(test_data, axis = -1, order = 2)

test_data = np.array(test_data)
test_targets = np.array(test_targets)

score = model_2.evaluate(test_data, test_targets)

"""
test
"""
test_targets_predicted = model_2.predict(test_data)
print ('predicted_value: ', test_targets_predicted[1])
print ('true_value: ', test_targets[1])

"""
print(test_targets_predicted[1]*std+mean)
print(test_targets[1]*std+mean)

for item in test_targets_predicted:
    print(item*std+mean)
"""
test_mse_score, test_mae_score = model_2.evaluate(test_data, test_targets)
print (test_mae_score, test_mse_score)
