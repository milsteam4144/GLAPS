from flask import Flask, jsonify
import Prediction

app = Flask(__name__)

@app.route('/GLAPS/<int:homeValue>/<string:stateCountyString>', methods=['GET'])
def yourfunctionname(stateCountyString, homeValue):
    prediction, predictionS, homeValue, homeValueS = Prediction.prediction(stateCountyString, homeValue)
    return jsonify(prediction, predictionS, homeValue, homeValueS)

if __name__ == '__main__':
    app.run(debug=True)

