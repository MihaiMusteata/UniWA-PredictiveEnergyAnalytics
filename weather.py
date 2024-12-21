import requests

# Mapping weather conditions based on the legend
CONDITIONS_MAPPING = {
    0: ["Sunny", "Clear"],
    1: [
        "Patchy rain possible", "Light rain", "Moderate rain at times", "Moderate rain",
        "Heavy rain at times", "Heavy rain", "Torrential rain shower", "Light drizzle",
        "Patchy light drizzle", "Moderate or heavy rain shower", "Light rain shower"
    ],
    2: [
        "Patchy snow possible", "Light snow", "Moderate snow", "Heavy snow",
        "Ice pellets", "Patchy light snow with thunder", "Moderate or heavy snow with thunder",
        "Light snow showers", "Moderate or heavy snow showers", "Blizzard", "Patchy sleet possible",
        "Light sleet", "Moderate or heavy sleet"
    ],
    3: ["Partly Cloudy", "Cloudy", "Overcast"]
}

def map_condition_to_legend(condition):
    for legend, conditions in CONDITIONS_MAPPING.items():
        if condition in conditions:
            return legend
    return condition

def get_coordinates_from_ip():
    # URL for detecting location by IP
    ipinfo_url = "https://ipinfo.io/json"

    try:
        # Perform GET request
        response = requests.get(ipinfo_url)
        response.raise_for_status()  # Raise error for status code > 400

        # Parse JSON data
        data = response.json()

        # Extract coordinates
        loc = data.get("loc", "")
        if loc:
            lat, lon = loc.split(",")
            return float(lat), float(lon)
        else:
            print("Coordinates not found in IP API response.")
            return None, None

    except requests.exceptions.RequestException as e:
        print(f"Error during geolocation request: {e}")
        return None, None

def get_weather_by_coordinates(lat, lon, api_key):
    # WeatherAPI endpoint URL
    base_url = "http://api.weatherapi.com/v1/current.json"

    # Request parameters
    params = {
        "key": api_key,
        "q": f"{lat},{lon}"
    }

    try:
        # Perform GET request
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise error for status code > 400

        # Parse JSON data
        data = response.json()

        # Extract relevant information
        temperature = data['current']['temp_c']
        humidity = data['current']['humidity']
        condition = map_condition_to_legend(data['current']['condition']['text'])

        return {
            "temperature_celsius": temperature,
            "humidity_percent": humidity,
            "weather_condition": condition,
            "weather_condition_label": data['current']['condition']['text']
        }

    except requests.exceptions.RequestException as e:
        print(f"Error during WeatherAPI request: {e}")
    except KeyError:
        print("The desired key was not found in the API response.")

def get_weather_data():
    # Enter your WeatherAPI key
    API_KEY = "your WeatherAPI key"
    # Get coordinates based on IP
    latitude, longitude = get_coordinates_from_ip()

    if latitude is not None and longitude is not None:
        # Call function to get weather data
        return get_weather_by_coordinates(latitude, longitude, API_KEY)

    return None

