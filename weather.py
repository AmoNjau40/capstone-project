import requests

def get_weather():

    url = (
        "https://api.open-meteo.com/v1/forecast?"
        "latitude=-1.17&longitude=36.83"
        "&current=temperature_2m,is_day,weather_code,wind_speed_10m"
    )

    response = requests.get(url)
    print(response.status_code)
    print(response.text)

    if response.status_code == 200:

        weather = response.json()

        current = weather["current"]

        temperature = current["temperature_2m"]
        is_day = current["is_day"]
        weather_code = current["weather_code"]
        wind_speed = current["wind_speed_10m"]

        if is_day == 1:
            day_time = "Day ☀️"
        else:
            day_time = "Night 🌙"

        if weather_code == 0:
            condition = "Clear ☀️"
        elif weather_code in [1, 2, 3]:
            condition = "Cloudy ☁️"
        elif weather_code in [51, 53, 55, 61, 63, 65]:
            condition = "Rainy 🌧"
        else:
            condition = "Other"

        return temperature, day_time, condition, wind_speed

    
    return None