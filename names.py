# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 13:46:34 2019

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

df = df.reset_index(['StateCountyName','Year'])
agroupDf=df.groupby(level='Year')


print(df1)