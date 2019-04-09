# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
import json
import requests

app = Flask(__name__)

app.config["DEBUG"] = True

result = []
@app.route("/", methods=["GET", "POST"])
def adder_page():
    errors = ""
    if request.method == "POST":
        County = None
        HomeVal = None
        try:
            County = request.form["County"]
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["County"])
        try:
            HomeVal = int(request.form["HomeVal"])
        except:
            errors += "<p>{!r} is not a number.</p>\n".format(request.form["HomeVal"])
        if County is not None and HomeVal is not None:
            result = getAPI()
            """
            homevalS = result[3]
            homeval= result[2]
            medvals = result[1]
            medval = result [0]
            """
            return '''
                <html>
                    <body>
                        <p>The medval is {result[0]}</p>
                        <p><a href="/">Click here to calculate again</a>
                    </body>
                </html>
            '''.format(result=result)

    return '''
        <html>
            <body>
                {errors}
                <p>Enter your Data:
                <form method="post" action='.'>
                    <p><input name="County" /></p>
                    <p><input name="HomeVal" /></p>
                    <p><input type="submit" value="Submit" /></p>
                </form>
            </body>
        </html>
    '''.format(errors=errors)

def getAPI():

    myreqs = {"HomeVal":request.form['HomeVal'], "County":request.form['County']}
    url = requests.get("http://127.0.0.1:5000/GLAPS", params=myreqs)
    responseJson = json.loads(url.text)

    return responseJson

if __name__ == '__main__':
    app.run(debug=True, port=8001)