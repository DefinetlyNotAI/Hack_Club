import geocoder
import requests
import json
import colorlog

# Configure colorlog for logging messages with colors
logger = colorlog.getLogger()
# Change to DEBUG if needed
logger.setLevel(colorlog.INFO)

handler = colorlog.StreamHandler()
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "red",
    },
)
handler.setFormatter(formatter)
logger.addHandler(handler)


class Obtain:
    @staticmethod
    def __get_api_key_from_json(file_path):
        """
        Reads an API key from a JSON file.

        Parameters:
        - file_path: str, the path to the JSON file containing the API key.

        Returns:
        - str: The API key read from the file.
        """
        try:
            with open(file_path, "r") as file:
                config_data = json.load(file)
                colorlog.debug(f"API Key successfully read from {file_path}.")
                # Convert the dictionary to a string representation before logging
                colorlog.debug("File Contents: " + json.dumps(config_data))
                API = config_data.get("apiKey", None)
                colorlog.debug(f"API Key: {API}")
                return API
        except FileNotFoundError:
            colorlog.error(f"File {file_path} not found.")
        except json.JSONDecodeError:
            colorlog.error(f"Unable to parse JSON in file {file_path}.")
        except KeyError:
            colorlog.error(f"Key 'apiKey' not found in file {file_path}.")
        except Exception as e:
            colorlog.error(f"An unexpected error occurred: {e}")

    def __get_location_and_weather(self):
        """
        Retrieves the current GPS coordinates and weather information for the user's location using the One Call API.

        Returns:
            str: A JSON string containing the combined location and weather information, including latitude, longitude, weather description, temperature, pressure, and humidity. Returns None if there was an error retrieving the API key, GPS coordinates, or weather data.

        Raises:
            Exception: If an unexpected error occurs during the execution of the function.
        """
        try:
            api_key = self.__get_api_key_from_json("api.json")
            if api_key is None:
                colorlog.error("Failed to retrieve API key.")

            # Get current GPS coordinates
            location = geocoder.ip("me")
            if location.latlng is None:
                colorlog.error("Unable to retrieve GPS coordinates.")

            latitude, longitude = location.latlng
            location_info = {"location": f"{latitude}, {longitude}"}
            colorlog.debug(f"Latitude: {latitude}, Longitude: {longitude}")

            # Corrected base URL to include the version number
            base_url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": "London,uk",  # Example city; replace with dynamic input if needed
                "appid": api_key,
                "units": "metric",
            }
            try:
                response = requests.get(base_url, params=params)
                response.raise_for_status()
                weather_data = response.json()
                weather_info = {
                    "weather": weather_data["weather"][0]["description"],
                    "temperature": weather_data["main"]["temp"],
                    "pressure": weather_data["main"]["pressure"],
                    "humidity": weather_data["main"]["humidity"],
                }
            except requests.exceptions.RequestException as e:
                colorlog.error(f"Failed to fetch weather data: {e}")

            # Combine location and weather info
            combined_info = {**location_info, **weather_info}
            return json.dumps(combined_info, indent=4)
        except Exception as e:
            colorlog.error(f"An error occurred: {e}")

    def wal(self):
        """
        WAL stands for Weather and Location, This is a wrapper function
        That includes error checks, etc.

        :return:
            str/bool: False boolean if an error occurs, else returns a JSON string
        """
        # Example usage
        result = self.__get_location_and_weather()
        if result is None:
            colorlog.error(
                "An error occurred: While fetching weather data and the response was NULL."
            )
        else:
            return str(result)


# Return the result, will return False if there was an error
print(Obtain().wal())
