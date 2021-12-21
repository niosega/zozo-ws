import requests
import urllib.parse
import json
import os

class Zoe:

    def __init__(self, myRenaultUser, myRenaultPass):
        self.myRenaultUser = myRenaultUser
        self.myRenaultPass = myRenaultPass
        self.gigyaURL = "https://accounts.eu1.gigya.com"
        self.gigyaAPI = "3_7PLksOyBRkHv126x5WhHb-5pqC1qFR8pQjxSeLB6nhAnPERTUlwnYoznHSxwX668" 
        self.kamareonURL = "https://api-wired-prod-1-euw1.wrd-aws.com"
        self.kamareonAPI = "Ae9FDWugRxZQAGm3Sxgk7uJn6Q4CGEA2"

    def encodeURIComponent(self, s):
        return urllib.parse.quote(s)

    def getStatus(self, endpoint, version = "2"):
        url = self.kamareonURL + '/commerce/v1/accounts/' + self.account_id + '/kamereon/kca/car-adapter/v' + version + '/cars/' + self.VIN + '/' + endpoint + '?country=FR'
        headers = {"x-gigya-id_token": self.gigyaJWTToken, "apikey": self.kamareonAPI, "Content-type": "application/vnd.api+json"}
        response = requests.get(url, headers=headers)
        return json.loads(response.text)

    def loadFromFile(self, filename):
        try:
            with open(filename, "r") as f:
                return f.read()
        except:
            return None

    def saveToFile(self, data, filename):
        with open(filename, "w") as f:
            f.write(data)

    def cleanPersonnalInfo(self):
        if os.path.exists("firststep.dta"):
            os.remove("firststep.dta")
        if os.path.exists("secondstep.dta"):
            os.remove("secondstep.dta")
        if os.path.exists("thirdstep.dta"):
            os.remove("thirdstep.dta")
        if os.path.exists("fourstep.dta"):
            os.remove("fourstep.dta")

    def getPersonnalInfo(self):
        # Save the result to a file, to avoid being annoyed by renault server quota limits.
        data = self.loadFromFile("firststep.dta")
        if data is None:
            url = self.gigyaURL + '/accounts.login?loginID=' + self.encodeURIComponent(self.myRenaultUser) + '&password=' + self.encodeURIComponent(self.myRenaultPass) + '&include=data&apiKey=' + self.gigyaAPI
            response = requests.get(url)
            data = response.text
            self.saveToFile(data, "firststep.dta")
        self.gigyaCookieValue = json.loads(data)["sessionInfo"]["cookieValue"]
        self.gigyaPersonID = json.loads(data)["data"]["personId"]

        # Save the result to a file, to avoid being annoyed by renault server quota limits.
        data = self.loadFromFile("secondstep.dta")
        if data is None:
            url = self.gigyaURL + '/accounts.getJWT?oauth_token=' + self.gigyaCookieValue + '&login_token=' + self.gigyaCookieValue + '&expiration=' + "87000" + '&fields=data.personId,data.gigyaDataCenter&ApiKey=' + self.gigyaAPI
            response = requests.get(url)
            data = response.text
            self.saveToFile(data, "secondstep.dta")
        self.gigyaJWTToken = json.loads(data)["id_token"]

        # Save the result to a file, to avoid being annoyed by renault server quota limits.
        data = self.loadFromFile("thirdstep.dta")
        if data is None:
            url = self.kamareonURL + '/commerce/v1/persons/' + self.gigyaPersonID + '?country=FR'
            headers = {"x-gigya-id_token": self.gigyaJWTToken, "apikey": self.kamareonAPI}
            response = requests.get(url, headers=headers)
            data = response.text
            self.saveToFile(data, "thirdstep.dta")
        self.account_id = json.loads(data)["accounts"][0]["accountId"]

        # Save the result to a file, to avoid being annoyed by renault server quota limits.
        data = self.loadFromFile("fourstep.dta")
        if data is None:
            url = self.kamareonURL + '/commerce/v1/accounts/' + self.account_id + '/vehicles?country=FR'
            headers = {"x-gigya-id_token": self.gigyaJWTToken, "apikey": self.kamareonAPI}
            response = requests.get(url, headers=headers)
            data = response.text
            self.saveToFile(data, "fourstep.dta")
        self.VIN = json.loads(data)["vehicleLinks"][0]["vin"]

    def batteryStatus(self):
        return self.getStatus("battery-status")
    
    def location(self):
        return self.getStatus("location", "1")

    def googleLocation(self):
        loc = self.location()
        lat = str(loc["data"]["attributes"]["gpsLatitude"])
        lon = str(loc["data"]["attributes"]["gpsLongitude"])
        return "https://www.google.com/maps/search/" + lat + "+" + lon
    
    def chargingSettings(self):
        return self.getStatus("charging-settings", "1")
    
    def cockpit(self):
        return self.getStatus("cockpit", "1")
    
    def hvacStatus(self):
        return self.getStatus("hvac-status", "1")
