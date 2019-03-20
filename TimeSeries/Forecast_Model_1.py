# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 12:24:48 2019

@author: canjurag4010
"""
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

"""
Get Data
"""
path = os.path.abspath("MinorLeague.db")
engine = create_engine("sqlite:///"+path, echo = False)#Set to false to git rid of log
#Link a session to the engine and initialize it
conn = engine.connect()

df = pd.read_sql_table('Detailed', conn)
df = df.drop(['CountyCode'], axis = 1)
df = df.drop(['StateCode'], axis = 1)
df = df.drop(['population'], axis = 1)
df = df.drop(['medianRealEstateTax'], axis = 1)
df = df.drop(['medianHouseholdCosts'], axis = 1)
df = df.drop(['totalHouses'], axis = 1)

print(df)

np.random.seed(seed=42)
"""
splits data into years
"""
train_range = df[df.Year < 2013].index
validate_range = df[(df.Year >= 2013) & (df.Year < 2015)].index
test_range = df[(df.Year >= 2015) & (df.Year < 2017)].index

fig, ax = plt.subplots(figsize=(18,6))
df.loc[train_range].plot(x="Year", y="medianHomeVal", ax=ax, label="train")
df.loc[validate_range].plot(x="Year", y="medianHomeVal", ax=ax, label="validate")
df.loc[test_range].plot(x="Year", y="medianHomeVal", ax=ax, label="test")

ax.axvline(pd.to_datetime(str(df.loc[validate_range].Year.medianHomeVal[0])), c='green', ls='--', lw=1)
plt.axvline(pd.to_datetime(str(df.loc[test_range].Year.medianHomeVal[0])), c='red', ls='--', lw=1)
plt.legend(loc='upper left')

plt.savefig('images/ann-split.png');

"""
normalizes data
"""
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))
data = scaler.fit_transform(df.medianHomeVal.astype(float).values.reshape(-1, 1));

"""
convert observations into seasonal learning data
"""
def build_seasonal_learning_sequences(data, indices, seasons=12):
    train, validate, test = indices
    
    X_train = np.empty(shape=(0, seasons))
    y_train = np.empty(shape=(0, seasons))
    
    X_val = np.empty(shape=(0, seasons))
    y_val = np.empty(shape=(0, seasons))
    
    X_test = np.empty(shape=(0, seasons))
    y_test = np.empty(shape=(0, seasons))
    
    for i in range(seasons, data.shape[0] - seasons):
        X = data[i - seasons:i].reshape(1,-1)
        y = data[i:i + seasons].reshape(1,-1)
        if i in train:
            X_train = np.concatenate((X_train, X), axis=0)
            y_train = np.concatenate((y_train, y), axis=0)
        elif i in validate:
            X_val = np.concatenate((X_val, X), axis=0)
            y_val = np.concatenate((y_val, y), axis=0)
        elif i in test:
            X_test = np.concatenate((X_test, X), axis=0)
            y_test = np.concatenate((y_test, y), axis=0)

    return X_train, y_train, X_val, y_val, X_test, y_test

"""
For our data we observe the yearly seasonality, thus we select $seasons=12$
"""
seasons = 12
indices = [train_range, validate_range, test_range]

X_train, y_train, X_val, y_val, X_test, y_test = build_seasonal_learning_sequences(
    data, indices, seasons)

from keras import backend as K

def r2_metric(y_true, y_pred):
    """Calculate R^2 statistics using observed and predicted tensors."""
    SS_res =  K.sum(K.square(y_true - y_pred)) 
    SS_tot = K.sum(K.square(y_true - K.mean(y_true))) 
    return (1 - SS_res/(SS_tot + K.epsilon()))


def theils_u_metric(y_true, y_pred):
    """Calculate Theil's U statistics using observed and predicted tensors."""
    SS_res =  K.mean(K.square(y_true - y_pred))
    SS_true = K.mean(K.square(y_true))
    SS_pred = K.mean(K.square(y_pred))
    
    return K.sqrt(SS_res / (SS_true * SS_pred))

from keras.layers import InputLayer, Dense, LSTM
from keras.models import Sequential
from keras.optimizers import SGD

"""
create Model
"""

sgd = SGD(lr=0.05, decay=1e-6, momentum=0.9, nesterov=False)

model = Sequential()
model.add(InputLayer(input_shape=(1, seasons), name="input"))
model.add(LSTM(4, name="hidden", activation='sigmoid', use_bias = True, bias_initializer='ones'))
model.add(Dense(seasons, name="output", activation='linear', use_bias = True, bias_initializer='ones'))
model.compile(loss='mean_squared_error',
              optimizer=sgd,
              metrics=["mae", "mse", r2_metric, theils_u_metric])


from IPython.display import SVG
from keras.utils import plot_model
from keras.utils.vis_utils import model_to_dot

plot_model(model, to_file=os.path.abspath('images/ann-model.png'))
SVG(model_to_dot(model).create(prog='dot', format='svg'))

num_of_epochs = 40
history = model.fit(
    X_train, y_train,
    epochs=num_of_epochs,
    batch_size=1,
    verbose=0,
    validation_data=(X_val, y_val));

fig, ax = plt.subplots(figsize=(18,6))
plt.plot(history.history["mean_squared_error"], label="train MSE")
plt.plot(history.history["val_mean_squared_error"], label="validation MSE")
plt.legend(loc='upper left')
plt.savefig('images/ann-val-history.png');

_, mae, mse, r2, u = model.evaluate(X_train, y_train, batch_size=1, verbose=0)

print("MAE (train): {:0.3f}".format(mae))
print("MSE (train): {:0.3f}".format(mse))
print("R2  (train): {:0.3f}".format(r2))
print("U   (train): {:0.3f}".format(u))

_, mae, mse, r2, u = model.evaluate(X_val, y_val, batch_size=1, verbose=0)

print("MAE (val): {:0.3f}".format(mae))
print("MSE (val): {:0.3f}".format(mse))
print("R2  (val): {:0.3f}".format(r2))
print("U   (val): {:0.3f}".format(u))

yhat_train = model.predict(X_train[::seasons])
yhat_val = model.predict(X_val[::seasons])
yhat_test = model.predict(X_test[::seasons])

yhat_train_unscaled = scaler.inverse_transform(yhat_train).flatten()
yhat_val_unscaled = scaler.inverse_transform(yhat_val).flatten()
yhat_test_unscaled = scaler.inverse_transform(yhat_test).flatten()

y_train_unscaled = scaler.inverse_transform(y_train[::seasons]).flatten()
y_val_unscaled = scaler.inverse_transform(y_val[::seasons]).flatten()
y_test_unscaled = scaler.inverse_transform(y_test[::seasons]).flatten()

"""
evaluate forecast
"""

from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

def theils_u_metric(y_true, y_pred):
    """Calculate Theil's U statistics using observed and predicted vectors."""
    SS_res =  np.mean(np.square(y_true - y_pred))
    SS_true = np.mean(np.square(y_true))
    SS_pred = np.mean(np.square(y_pred))
    
    return np.sqrt(SS_res / (SS_true * SS_pred))

mae = mean_absolute_error(y_test_unscaled, yhat_test_unscaled)
mse = mean_squared_error(y_test_unscaled, yhat_test_unscaled)
r2 = r2_score(y_test_unscaled, yhat_test_unscaled)
u = theils_u_metric(y_test_unscaled, yhat_test_unscaled)

print("MAE (test): {:0.0f}".format(mae))
print("MSE (test): {:0.0f}".format(mse))
print("R2  (test): {:0.3f}".format(r2))
print("U   (test): {:0.6f}".format(u))


fig, ax = plt.subplots(figsize=(18,6))
ax.plot(pd.to_datetime(df.loc[train_range].period.values)[seasons:], yhat_train_unscaled,
        color="red", label="train")
ax.plot(pd.to_datetime(df.loc[validate_range].period.values), yhat_val_unscaled,
        color="green", label="val")
ax.plot(pd.to_datetime(df.loc[test_range].period.values), yhat_test_unscaled,
        color="blue", label="test")

ax.axvline(pd.to_datetime(str(df.loc[validate_range].period.values[0])), c='green', ls='--', lw=1)
plt.axvline(pd.to_datetime(str(df.loc[test_range].period.values[0])), c='red', ls='--', lw=1)
df.plot(x="period", y="value", ax=ax, label="observed")

plt.legend(loc='best')
plt.title('Compare forecast for the overall period')

plt.savefig('images/ann-compare-forecast-overall.png')
plt.show();

fig, ax = plt.subplots(figsize=(18,6))
ax.plot(pd.to_datetime(df.loc[validate_range].period.values), yhat_val_unscaled,
        color="blue", label="predicted")

df.loc[validate_range].plot(x="period", y="value", ax=ax, label="observed")
plt.legend(loc='best')
plt.title('Compare forecast for the val range')

plt.savefig('images/ann-compare-forecast-valrange.png')
plt.show();

fig, ax = plt.subplots(figsize=(18,6))
ax.plot(pd.to_datetime(df.loc[test_range].period.values), yhat_test_unscaled,
        color="blue", label="predicted")

df.loc[test_range].plot(x="period", y="value", ax=ax, label="observed")
plt.legend(loc='best')
plt.title('Compare forecast for the test range')

plt.savefig('images/ann-compare-forecast-testrange.png')
plt.show();