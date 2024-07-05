import os
import requests

def get_weather_details(location: str):
    apiKey = os.environ.get("WEATHER_API_KEY", "")
    url = f"http://api.weatherapi.com/v1/current.json?key={apiKey}&q={location},Lagos&aqi=no"
    
    response = requests.get(url)
    return response.json()

def get_inspirational_quote():
    url = f"https://zenquotes.io/api/random/"
    response = requests.get(url)
    return response.json()[0]

def get_crypto_prices():
    pass