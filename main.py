import requests
import os
from twilio.rest import Client


API_KEY = os.environ.get("OWM_API_KEY")
MY_LAT = -32.926670
MY_LON = 151.780014
account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

parameters = {
    "lat": MY_LAT,
    "lon": MY_LON,
    "appid": API_KEY,
    "exclude": "current,minutely,daily",
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/onecall", params=parameters)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    weather_code = hour_data["weather"][0]["id"]
    if weather_code < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body ="It's going to rain 🌧 today. Remember to take an umbrella when you go out.☂️",
        from_= os.environ.get("FROM_NUMBER"),
        to = os.environ.get("To_NUMBER"),
    )
    print(message.status)