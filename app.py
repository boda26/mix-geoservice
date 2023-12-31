from flask import Flask, render_template, request, jsonify
import requests
import os
import json

app = Flask(__name__)

# Route for "/" (frontend):
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/city')
def index_city():
    return render_template("index_plain.html")

# Route for "/MIX" (middleware):
@app.route('/MIX', methods=["POST"])
def POST_location():
    location = request.form["location"]
    
    if ',' not in location:
        return jsonify({"error": "Invalid Coordinate Input!"}), 500
    
    location = location.replace(' ', '')
    location = location.split(',')

    if len(location) != 2:
        return jsonify({"error": "Invalid Coordinate Input!"}), 500

    lat, lon = location[0], location[1]

    # weather_url = os.getenv("WEATHER_URL")
    ninjas_key = os.getenv("NINJAS_KEY")
    geo_url = os.getenv("GEOAPI_URL")
    geo_url = f'{geo_url}lat={lat}&lon={lon}'
    r = requests.get(geo_url, headers={'X-Api-Key': ninjas_key}).json()
    print(r)
    if "error" in r:
        return jsonify (
            errorMessage = 'Invalid geographical location!'
        )
    js = json.dumps(r[0])
    js = json.loads(js)

    return js, 200