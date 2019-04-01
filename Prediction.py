from keras.models import load_model
import os
import pandas as pd
from sqlalchemy import create_engine
from sklearn.externals import joblib

#gets the line of current data from table to use for prediction

def getPredictionInput(stateCountyString):

    #gets table from db
    dbPath = os.path.abspath("MinorLeague.db")
    engine = create_engine("sqlite:///" + dbPath, echo=False)  # Set to false to git rid of log
    # Link a session to the engine and initialize it
    conn = engine.connect()

    df = pd.read_sql_table('all_3_Data', conn)

    #gets all lines with 2017
    yrLines = df.loc[df['Year'] == 2017]
    #gets line for specific county and state
    line = yrLines.loc[yrLines['State_Cty'] == stateCountyString]

    #drops the unneeded columns
    line = line.drop(['medianHomeVal', 'Year', 'State_Cty', 'CountyCode'], axis = 1)

    # loads the saved scalers that were used for the model
    scaler_data = joblib.load("sc_data.save")

    scaledInput = scaler_data.transform(line)

    print(scaledInput)

    return scaledInput

def prediction(stateCountyString, Homeval):
    """
    This checks the version of keras of the saved model
    import h5py

    f = h5py.File('960.h5', 'r')
    print(f.attrs.get('keras_version'))
    """
    # loads the saved scalers that were used for the model
    scaler_targets = joblib.load("sc_targets.save")

    #gets the path for the model
    path = os.path.abspath('model_2017_4.h5')

    #loads the model
    model = load_model(path)

    scaledInput = getPredictionInput(stateCountyString)

    if scaledInput[0][14] == 0:
        # Make a prediction with the neural network
        prediction = model.predict(scaledInput)

        prediction = scaler_targets.inverse_transform(prediction)
        # Grab just the first element of the first prediction (since that's the only have one)
        prediction = (prediction[0][0])

        #changes from not having stadium to having Stadium
        scaledInput[0][14] = 1

        predictionS = model.predict(scaledInput)

        predictionS = scaler_targets.inverse_transform(predictionS)
        predictionS = (predictionS[0][0])

        HomevalS = Homeval*(1+(prediction-predictionS)/prediction);

    elif scaledInput[0][14] == 1:

        predictionS = model.predict(scaledInput)

        predictionS = scaler_targets.inverse_transform(predictionS)
        predictionS = (predictionS[0][0])

        HomevalS = Homeval

        #changes to not having a stadium
        scaledInput[0][14] = 0

        # Make a prediction with the neural network
        prediction = model.predict(scaledInput)

        prediction = scaler_targets.inverse_transform(prediction)
        # Grab just the first element of the first prediction (since that's the only have one)
        prediction = (prediction[0][0])

        Homeval = Homeval*(1+(predictionS - prediction)/predictionS)

    return prediction, predictionS, Homeval, HomevalS
"""
    print("Median Home Value with Stadium - ${}".format(predictionS))
    print("Median Home Value without Stadium - ${}".format(prediction))
    print("Your Home Value with Stadium - ${}".format(HomevalS))
    print("Your Home Value without Stadium - ${}".format(Homeval))

prediction('Barrow County, Georgia', 150000)
"""
