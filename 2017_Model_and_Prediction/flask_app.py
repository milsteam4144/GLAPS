from flask import Flask, jsonify
import Prediction

app = Flask(__name__)

@app.route('/GLAPS/<int:homeValue>/<string:stateCountyString>', methods=['GET'])
def yourfunctionname(stateCountyString, homeValue):
    prediction, predictionS, homeValue, homeValueS = Prediction.prediction(stateCountyString, homeValue)
    valList = []
    valList.append(int(prediction))
    valList.append(int(predictionS))
    valList.append(int(homeValue))
    valList.append(int(homeValueS))
    return jsonify(valList)

if __name__ == '__main__':
    app.run(debug=True)



