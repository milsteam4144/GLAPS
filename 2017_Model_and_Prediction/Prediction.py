from keras.models import load_model
import os
import pandas as pd
from sqlalchemy import create_engine

stateCountyString = 'Barrow County, Georgia'

input = getPredictionInput(stateCountyString)

#ToDo: scaledInput = PickledScalar(input)
#ToDo: add if statement to change stadium to 1 or 09+


path = os.path.abspath("model_4.h5")
model = load_model(path)

# Make a prediction with the neural network
prediction = model.predict(scaledInput)

# Grab just the first element of the first prediction (since that's the only have one)
prediction = prediction[0][0]

prediction = inverse_scalar(prediction)

predictionS = model.predict(scaledInput)

# Grab just the first element of the first prediction (since that's the only have one)
predictionS = predictionS[0][0]

predictionS = inverse_scalar(predictionS)


print("Median Home Value with Stadium - ${}".format(predictionS))
print("Median Home Value without Stadium - ${}".format(prediction))

#Todo: determine calculation for the person's home can't think now

print("Your Home Value with Stadium - ${}".format(prediction))
print("Your Home Value without Stadium - ${}".format(prediction))

def getStateandCountyCode(stateCountyString, conn):

    df = pd.read_sql_table('State_Counties', conn)

    line = df.loc[df['StateAndCounty'] == StateCountyString]

    stateCode = line['StateCode']

    countyCode = line['CountyCode']

    return stateCode, countyCode

def getPredictionInput(stateCountyString):

    dbPath = os.path.abspath("MinorLeague.db")
    engine = create_engine("sqlite:///" + dbPath, echo=False)  # Set to false to git rid of log
    # Link a session to the engine and initialize it
    conn = engine.connect()

    state, county = getStateandCountyCode(stateCountyString, conn)

    df = pd.read_sql_table('all_3_Data', conn)

    df = df.drop(['medianHomeVal'], axis = 1)

    line = df.loc[df['StateCode'] == state and df['CountyCode'] == county]

    return line

