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
#import keras.callbacks 

"""
Print versions of tensorflow anr keras
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

df = pd.read_sql_table('Detailed', conn)
df = df.drop(['locationID'], axis = 1)
df = df.drop(['year'], axis = 1)

#randomly takes 80% of the DB dataset and places it in train
train = df.sample(frac = 0.7, random_state=700)

#places remaining items in test db
test = df.drop(train.index)

"""
normalize train data
"""

mean = train.mean()
std = train.std()
train = (train-mean)/std

train.describe()

"""
features
"""
train_targets = train['medianHomeVal']
train_data = train.drop(['medianHomeVal'], axis = 1)

#makes data numpy arrays
train_data=np.array(train_data)
train_targets = np.array(train_targets)

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
inputs = Input(shape=(4,))
preds = Dense(1,activation='linear')(inputs)

model_2 = Model(inputs=inputs,outputs=preds)
#sgd=keras.optimezer.SGD()
model_2.compile(optimizer='adam', loss = 'mse', metrics=['mse'])

"""
Train Model
"""

#Train the model
hist = model_2.fit(train_data,train_targets,batch_size=15, epochs = 490)

#visualizing losses and accuracy
num_epochs = 490
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
mean = test.mean()
std = test.std()
test = (test-mean)/std

test_targets = test['medianHomeVal']
test_data = test.drop(['medianHomeVal'], axis = 1)

test_data = np.array(test_data)
test_targets = np.array(test_targets)
score = model_2.evaluate(test_data, test_targets)

"""
test
"""
test_targets_predicted=model_2.predict(test_data)
print ('predicted_value: ', test_targets_predicted)
print ('true_value: ', test_targets)
for item in test_targets_predicted:
    print(item*std+mean)

