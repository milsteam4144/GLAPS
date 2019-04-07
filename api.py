from flask import Flask, jsonify, request
import Prediction2

app = Flask(__name__)



@app.route('/GLAPS', methods=['GET'])
def GLAPS():

    if 'HomeVal' and 'County' in request.args:
        homeValue = int(request.args['HomeVal'])
        stateCountyString = request.args['County']

        prediction, predictionS, homeValue, homeValueS = Prediction2.prediction(stateCountyString, homeValue)

        prediction = int(prediction)
        predictionS = int(predictionS)
        homeValue = int(homeValue)
        homeValueS = int(homeValueS)

        Values = [{'MedHomeVal': prediction, 'MedHomeValStad': predictionS,'HomeVal': homeValue,'HomeValStad': homeValueS}]

    return jsonify(Values)

if __name__ == '__main__':
    app.run(debug=True)



