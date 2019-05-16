from keras.models import load_model
import os
import pandas as pd
import json
from sqlalchemy import create_engine
from sklearn.externals import joblib
from oauth2client.client import GoogleCredentials
import googleapiclient.discovery

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

    input = scaledInput[0].tolist()

    return input

def getModelPrediction(scaledInput):

    print(scaledInput)

    # Change this values to match your project
    PROJECT_ID = "sound-berm-236202"
    MODEL_NAME = "glaps2"
    CREDENTIALS_FILE = "credentials.json"

    # These are the values we want a prediction for
    inputs_for_prediction = [{"input":scaledInput}]

    print(inputs_for_prediction)

    # Connect to the Google Cloud-ML Service
    credentials = GoogleCredentials.from_stream(CREDENTIALS_FILE)
    service = googleapiclient.discovery.build('ml', 'v1', credentials=credentials)

    # Connect to our Prediction Model
    name = 'projects/{}/models/{}'.format(PROJECT_ID, MODEL_NAME)
    response = service.projects().predict(
        name=name,
        body={'instances': inputs_for_prediction}
    ).execute()

    # Report any errors
    if 'error' in response:
        raise RuntimeError(response['error'])

    # Grab the results from the response object
    results = response['predictions']

    # gets the line of current data from table to use for prediction

    return results

def prediction(stateCountyString, Homeval):
    """
    This checks the version of keras of the saved model
    import h5py

    f = h5py.File('Model_2017_4.h5', 'r')
    print(f.attrs.get('keras_version'))
    """
    # loads the saved scalers that were used for the model
    scaler_targets = joblib.load("sc_targets.save")

    #gets the path for the model
    path = os.path.abspath('model_2017_4.h5')

    #loads the model
    model = load_model(path)

    scaledInput = getPredictionInput(stateCountyString)

    prediction = getModelPrediction(scaledInput)

    print(prediction)
    """
    if scaledInput[14] == 0:
        # Make a prediction with the neural network
        prediction = getModelPrediction(scaledInput)

        prediction = scaler_targets.inverse_transform(prediction)
        # Grab just the first element of the first prediction (since that's the only have one)
        prediction = (prediction[0][0])

        #changes from not having stadium to having Stadium
        scaledInput[14] = 1

        predictionS = getModelPrediction(scaledInput)

        predictionS = scaler_targets.inverse_transform(predictionS)
        predictionS = (predictionS[0][0])

        # percent of change (V2-V1)/|V1|
        HomevalS = HomevalS = Homeval*(1+((predictionS-prediction)/prediction))

    elif scaledInput[14] == 1:

        predictionS = getModelPrediction(scaledInput)

        predictionS = scaler_targets.inverse_transform(predictionS)
        predictionS = (predictionS[0][0])

        HomevalS = Homeval

        #changes to not having a stadium
        scaledInput[14] = 0

        # Make a prediction with the neural network
        prediction = getModelPrediction(scaledInput)

        prediction = scaler_targets.inverse_transform(prediction)
        # Grab just the first element of the first prediction (since that's the only have one)
        prediction = (prediction[0][0])

        Homeval = Homeval*(1+((prediction - predictionS)/predictionS))

    print("Median Home Value with Stadium - ${}".format(predictionS))
    print("Median Home Value without Stadium - ${}".format(prediction))
    print("Your Home Value with Stadium - ${}".format(HomevalS))
    print("Your Home Value without Stadium - ${}".format(Homeval))


    return prediction, predictionS, Homeval, HomevalS
"""

prediction('Barrow County, Georgia', 150000)
