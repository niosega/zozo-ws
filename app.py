from flask import Flask, json, jsonify
from zozo import Zoe
import os

app = Flask(__name__)
myRenaultUser = os.getenv("RENAULT_USER")
myRenaultPass = os.getenv("RENAULT_PASS")
zoe = Zoe(myRenaultUser, myRenaultPass)
zoe.getPersonnalInfo()

@app.route("/")
def index():
    return "Welcome to the ZOZO-WS homepage !"

@app.route("/api/status")
def status():
    return jsonify(zoe.batteryStatus()["data"]["attributes"])

@app.route("/api/location")
def location():
    loc = zoe.location()
    lat = str(loc["data"]["attributes"]["gpsLatitude"])
    lon = str(loc["data"]["attributes"]["gpsLongitude"])
    return jsonify({"lat": lat, "lon": lon})

@app.route("/api/clean")
def clean():
    zoe.cleanPersonnalInfo()
    return jsonify({"state": True})

app.run(host='0.0.0.0', debug=True)