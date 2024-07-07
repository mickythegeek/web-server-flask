# app.py
from flask import Flask, request, jsonify
import requests, os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
@app.route('/api/hello', methods=['GET'])

def tellClient():
    # Client's Name and IP Address
    visitor_name = request.args.get('visitor_name', 'Guest')
    client_ip = request.remote_addr

    # Clients Location
    ipinfo_api_key = os.getenv("location_api")
    response = requests.get(f'https://ipinfo.io/{client_ip}/json?token={ipinfo_api_key}')
    location_data = response.json()
    location = location_data.get('city')

    #Temperature of said location
    api_key = os.getenv("temperature_api")
    response = requests.get(f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}')
    weather_data = response.json()
    temperature = weather_data['current']['temp_c']



    greeting = f"Hello, {visitor_name}! The temperature is {temperature} degrees Celsius in {location}."

    return jsonify({
        'client_ip': client_ip,
        'location': location,
        'greeting': greeting
    })

if __name__ == '__main__':
    app.run(debug=True)
