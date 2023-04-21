from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
from markupsafe import escape
import datetime
# import Adafruit_DHT

app = Flask(__name__)

now = datetime.datetime.now()
timestring = now.strftime("%Y-%m-%d %H:%M")
global keepPublishing
keepPublishing = True

@app.route("/")
def main():
    templateData = {
    "time": now,
    "title": "Rest_API",
    "isPublishing": False
    }
    return render_template("index.html", **templateData)

@app.route("/sensorData")
def sensorData():
    hum, temp = 0,1
    # hum, temp = Adafruit_DHT.read_retry(11, 4)
    if hum is not None and temp is not None:
        return jsonify({'temperature': temp,'humidity':hum})
    else:
        return jsonify({'error': 'Sensor not working.'})

@app.route("/publish", methods=['POST'])
def publish():
    writeApi = request.form.get("writeApi")
    hum, temp = 0,1
    # hum, temp = Adafruit_DHT.read_retry(11, 4)
    data = "field1="+str(temp)+"&field2="+str(hum)+"&status=mqttpublish"
    pub_data = "Temperature = {}, Humidity = {}".format(temp,hum)
    if hum is not None and temp is not None:
        requests.get("https://api.thingspeak.com/update?api_key="+writeApi+"&"+data)
        templateData = {
            "time": now,
            "title": "Rest_API",
            "isPublishing": True,
            "writeApi": writeApi,
            "data": pub_data
        }
    else:
        templateData = {
            "time": now,
            "title": "Rest_API",
            "isPublishing": False
        }
    return render_template("index.html", **templateData)

if __name__ == '__main__':
    app.run(debug=True)

