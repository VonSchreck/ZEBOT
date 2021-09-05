from flask import Flask, request, make_response, jsonify
import requests
import json
from geopy.geocoders import Nominatim

app = Flask(__name__)

API_KEY = '39bca8fd0da57286b1cd6d726ee2b6f9'

@app.route('/')
def index():
    return 'Hello World!'

def results():
    req = request.get_json(force=True)

    action = req.get('queryResult').get('action')

    result = req.get("queryResult")
    parameters = result.get("parameters")

    if parameters.get('location').get('city'):
        geolocator = Nominatim(user_agent='weather-bot')
        location = geolocator.geocode(parameters.get('location').get('city'))
        lat = location.latitude
        long = location.longitude
        weather_req = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}'.format(lat, long,    API_KEY))
        current_weather = json.loads(weather_req.text)['current']
        temp = round(current_weather['temp'] - 273.15)
        feels_like = round(current_weather['feels_like'] - 273.15)
        clouds = current_weather['clouds']
        wind_speed = current_weather['wind_speed']
        weather_description = current_weather["weather"][0]["main"]
        humidity = current_weather["humidity"]
        pressure = current_weather["pressure"]

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Морось \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }


    if weather_description in code_to_smile:
        wd = code_to_smile[weather_description]
    else:
        wd = ""

    return {'fulfillmentText': 'Сейчас температура воздуха {} градусов \n Ощущается как {} градусов \n Облачность - {}% \n Скорость ветра - {}м/с \n Влажность - {} %\n Давление - {} мм.рт.ст \n {}'.format(str(temp), str(feels_like), str(clouds), str(wind_speed), str(humidity), str(pressure), str(wd))}


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    return make_response(jsonify(results()))

if __name__ == '__main__':
   app.run(debug=True)


