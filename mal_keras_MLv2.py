import json
from urllib.request import urlopen
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import MetaData, Table
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy import Index
from sqlalchemy.orm import relationship, backref
import logging
from sqlalchemy.orm import sessionmaker
import numpy as np
import pandas as pd
from keras import models, layers, callbacks
import tensorflow as tf
import keras



path = os.path.abspath("MinorLeague.db")
#dir_path = os.path.dirname(os.path.realpath("/MinorLeague/MinorLeague.db"))
#Define declarative base class
Base = declarative_base()
engine = create_engine("sqlite:///"+path, echo = False)#Set to false to git rid of log
#Link a session to the engine and initialize it
conn = engine.connect()
metadata = Base.metadata


Session = sessionmaker(bind=engine)
session = Session()


df = pd.read_sql_table('cumb_County', conn)
#df = pd.read_sql_table('Subject', conn)
df = df.drop(['meanIncome'], axis = 1)
df = df.drop(['CountyCode'], axis = 1)
df = df.drop(['StateCode'], axis = 1)

#Convert the StateCodes from strings to numbers
#df['StateCode'] = pd.to_numeric(df['StateCode'], errors='coerce').fillna(0)
#df['CountyCode'] = pd.to_numeric(df['CountyCode'], errors='coerce').fillna(0)


#randomly takes half of the DB dataset and places it in train
train = df.sample(frac = 0.5)
train_targets = train['medianHomeVal']

train_data = train.drop(['medianHomeVal'], axis = 1)

#places remaining items in test db
test = df.drop(train_data.index)
#removes final column which is the one that will be predicted

test_targets = test['medianHomeVal']
test_data = test.drop(['medianHomeVal'], axis = 1)



#Normalize the data

'''

train_data = np.array(train_data)
train_targets = np.array(train_targets)
test_data = np.array(test_data)
test_targets = np.array(test_targets)
'''
train_data = tf.keras.utils.normalize(train_data, axis = -1, order = 2)
test_data = tf.keras.utils.normalize(test_data, axis = -1, order = 2)
#train_targets = tf.keras.utils.normalize(train_targets, axis = 0, order = 2)
#test_targets = tf.keras.utils.normalize(test_targets, axis = 0, order = 2)




print("Train Data Shape: ", train_data.shape)
print("Test Data Shape: ", test_data.shape)

print("Train Targets Shape: ", train_targets.shape)
print ("Test Targets Shape: ", test_targets.shape)




def build_model():
    model = models.Sequential()
    model.add(layers.Dense(700, activation='relu', input_shape=(train_data.shape[1],)))
    model.add(layers.Dense(500, activation='relu'))
    model.add(layers.Dense(1))
    model.compile(optimizer='adadelta', loss='mse', metrics=['mae'])
    return model

model = build_model()
model.fit(train_data, train_targets,
epochs=100, batch_size=20, verbose=0)
test_mse_score, test_mae_score = model.evaluate(test_data, test_targets)

print(test_mae_score)





