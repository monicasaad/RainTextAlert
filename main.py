import requests
import os
from twilio.rest import Client


# constants
MY_API_KEY = os.environ.get("OWM_API_KEY")  # open weather map
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"  # open weather map endpoint
ACCOUNT_SID = ""  # twillio key
AUTH_TOKEN = os.environ.get("TWILLIO_AUTH_TOKEN")


parameters = {
    "lat": 42.984924,
    "lon": -81.245277,
    "appid": MY_API_KEY
}

response = requests.get(url=OWM_ENDPOINT, params=parameters)
response.raise_for_status()  # check for exceptions

data = response.json()  # extract json data

today_data = data["list"][:5]  # slice up to data for next 12 hours

# boolean to determine weather an umbrella is needed
umbrella_needed = False

# list to hold all weather condition codes
codes_list = []
for time in range(len(today_data)):
    code = today_data[time]["weather"][0]["id"]
    # if the condition code is < 700 (rainy condition codes), set umbrella_needed to true
    if code < 700:
        umbrella_needed = True
    codes_list.append(code)

if umbrella_needed:
    # set up twillio client to send sms notification
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    # message for sms notification
    message = client.messages \
        .create(
        body="It's going to rain today! Bring an umbrella ☂️",
        from_="+12121212121", #twilio number
        to="+11234567890" #forwarding phone number
    )

    # print status (queued means successful)
    print(message.status)
