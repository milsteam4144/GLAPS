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
Gets data from DB
"""
path = os.path.abspath("MinorLeague.db")
engine = create_engine("sqlite:///"+path, echo = False)#Set to false to git rid of log
#Link a session to the engine and initialize it
conn = engine.connect()

df = pd.read_sql_table('Detailed', conn)
df = df[:800]

population = df['population']
medianRealEstateTax = df['medianRealEstateTax']
medianHouseholdCost = df['medianHouseholdCosts']
totalHouses = df['totalHouses']
medianHomeValues = df['medianHomeVal']

def w_sum(a,b):
    assert(len(a) == len(b))
    output = 0
    for i in range(len(a)):
        output += (a[i] * b[i])
    return output

weights = [0.1, 0.2, 0.1, 0.2]
    
def neural_network(input, weights):
    pred = w_sum(input,weights)
    return pred
"""
population = np.array(population)
medianRealEstateTax = np.array(medianRealEstateTax)
medianHouseholdCost = np.array(medianHouseholdCost)
totalHouses = np.array(totalHouses)
medianHomeValues = np.array(medianHomeValues)
"""
# Input corresponds to every entry
# for the first game of the season.
print (population[0])

input = [population[0],medianRealEstateTax[0],medianHouseholdCost[0],totalHouses[0]]
pred = neural_network(input,weights)

print(pred)
