import sqlite3
conn = sqlite3.connect("weatherlocation.db")
import requests
from flask import Flask, request,render_template


app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/zipcode')
def weather_city():
    API_key = 'b4012066f7bd668f5dbeef89d3f61fa1'
    zipcode =77058
    url = f'http://api.openweathermap.org/data/2.5/weather?zip={zipcode},us&appid={API_key}'
    print(url)
    response = requests.get(url).json()
    forecast = response.get("weather",{})
    for i in forecast:
        result = i['description']
    temperature = response.get('main', {}).get('temp')
    minimum_temperature = response.get('main',{}).get('temp_min')
    maximum_temperature = response.get('main',{}).get('temp_max')
    humidity = response.get('main',{}).get('humidity')
    wind_speed = response.get('wind',{}).get('speed')
    return render_template("home.html")
if __name__ == '__main__':
    app.run(debug=True)



