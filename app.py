from flask import Flask, render_template, request, jsonify
import requests
import os
import json
import redis

# redis-start-server

app = Flask(__name__)
rds = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# Route for "/" (frontend):
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/city')
def index_city():
    return render_template("index_city.html")

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

    rds_key = lat + ' ' + lon
    if rds.exists(rds_key):
        js = rds.get(rds_key)
        js = json.loads(js)
        print('redis cache hit!')
        return js, 200

    # weather_url = os.getenv("WEATHER_URL")
    ninjas_key = os.getenv("NINJAS_KEY")
    geo_url = os.getenv("GEOAPI_URL")
    geo_url = f'{geo_url}lat={lat}&lon={lon}'
    r = requests.get(geo_url, headers={'X-Api-Key': ninjas_key}).json()
    if "error" in r:
        return jsonify (
            errorMessage = 'Invalid geographical location!'
        )
    js = json.dumps(r[0])
    js = json.loads(js)

    city = js["name"]
    city_url = os.getenv("CITY_URL")
    city_url = f'{city_url}{city}'
    r1 = requests.get(city_url, headers={'X-Api-Key': ninjas_key}).json()
    if r1 != []:
        js1 = json.dumps(r1[0])
        js1 = json.loads(js1)
        js.update(js1)

    weather_url = os.getenv("WEATHER_URL")
    weather_url = f'{weather_url}{city}'
    r2 = requests.get(weather_url, headers={'X-Api-Key': ninjas_key}).json()
    if "error" not in r2:
        js2 = json.dumps(r2)
        js2 = json.loads(js2)
        js['weather information'] = js2
    
    timezone_url = os.getenv("TIMEZONE_URL")
    timezone_url = f'{timezone_url}{city}'
    r3 = requests.get(timezone_url, headers={'X-Api-Key': ninjas_key}).json()
    if "error" not in r3:
        js3 = json.dumps(r3)
        js3 = json.loads(js3)
        js['timezone'] = js3['timezone']
        
    rds_val = json.dumps(js)
    rds.set(rds_key, rds_val)
    
    return js, 200


@app.route('/City', methods=["POST"])
def POST_city():
    location = request.form["location"]
    location = location.lower()
    location = location.capitalize()

    if rds.exists(location):
        js = rds.get(location)
        js = json.loads(js)
        print('redis cache hit!')
        return js, 200

    ninjas_key = os.getenv("NINJAS_KEY")
    city_url = os.getenv("CITY_URL")
    city_url = f'{city_url}{location}'
    r = requests.get(city_url, headers={'X-Api-Key': ninjas_key}).json()
    print(r)
    if r == []:
        return jsonify (
            errorMessage = 'Invalid city!'
        )
    js = json.dumps(r[0])
    js = json.loads(js)

    weather_url = os.getenv("WEATHER_URL")
    weather_url = f'{weather_url}{location}'
    r2 = requests.get(weather_url, headers={'X-Api-Key': ninjas_key}).json()
    if "error" not in r2:
        js2 = json.dumps(r2)
        js2 = json.loads(js2)
        js['weather information'] = js2
    
    timezone_url = os.getenv("TIMEZONE_URL")
    timezone_url = f'{timezone_url}{location}'
    r3 = requests.get(timezone_url, headers={'X-Api-Key': ninjas_key}).json()
    if "error" not in r3:
        js3 = json.dumps(r3)
        js3 = json.loads(js3)
        js['timezone'] = js3['timezone']
    
    rds_val = json.dumps(js)
    rds.set(location, rds_val)

    return js, 200