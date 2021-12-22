from flask import Flask, json, jsonify, render_template
from zozo import Zoe
import os
import datetime

app = Flask(__name__)
myRenaultUser = os.getenv("RENAULT_USER")
myRenaultPass = os.getenv("RENAULT_PASS")
zoe = Zoe(myRenaultUser, myRenaultPass)
zoe.getPersonnalInfo()

@app.route("/")
def index():
    status = zoe.batteryStatus()["data"]["attributes"]
    infos = []
    infos.append(("Niveau Batterie", status["batteryLevel"]))
    infos.append(("Autonomie", status["batteryAutonomy"]))
    infos.append(("Branché ?", "Oui" if status["plugStatus"] == 1 else "Non"))
    infos.append(("En charge ?", "Oui" if status["chargingStatus"] == 1.0 else "Non"))
    infos.append(("Temps restant", str(datetime.timedelta(minutes=status["chargingRemainingTime"]))))

    loc = zoe.location()
    lat = str(loc["data"]["attributes"]["gpsLatitude"])
    lon = str(loc["data"]["attributes"]["gpsLongitude"])
    return render_template("index.html", infos=infos, lat=lat, lon=lon)

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
    zoe.getPersonnalInfo()
    return jsonify({"state": True})

app.run(host='0.0.0.0', debug=True)