from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import json
from json.decoder import JSONDecodeError
import ssl
from typing import Literal, TypeAlias
import urllib.request
from urllib.error import URLError
import os
import config

from coordinates import Coordinates
from exceptions import ApiServiceError 

class WeatherType(Enum):
    Thunderstorm = "Гроза"
    Drizzle = "Изморось"
    Rain = "Дождь"
    Snow = "Снег"
    Clear = "Ясно"
    Fog = "Туман"
    Clouds = "Облачно"
    

Celsius: TypeAlias = int

@dataclass(slots=True, frozen=True)
class Weather:
    temperature: Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime
    city: str

def get_weather(coordinates: Coordinates) -> Weather:
    """Requests weather in OpenWeather API and returns it"""
    openweather_response = _get_openweather_response(
        longitude=coordinates.longitude, latitude=coordinates.latitude)
    weather = _parse_openweather_response(openweather_response)
    return weather

def _get_openweather_response(latitude: float, longitude: float) -> str:
    ssl._create_default_https_context = ssl._create_unverified_context
    url = config.OPENWEATHER_URL.format(
        latitude=latitude, longitude=longitude)
    try:
        return urllib.request.urlopen(url).read()
    except URLError:
        raise ApiServiceError

def _parse_openweather_response(openweather_response: str) -> Weather:
    try:
        openweather_dict = json.loads(openweather_response)
    except JSONDecodeError:
        raise ApiServiceError
    return Weather(
        temperature=_parse_temperature(openweather_dict),
        weather_type=_parse_weather_type(openweather_dict),
        sunrise=_parse_sun_time(openweather_dict, "sunrise"),
        sunset=_parse_sun_time(openweather_dict, "sunset"),
        city=_parse_city(openweather_dict)
    )

def _parse_temperature(openweather_dict: dict) -> Celsius:
    return round(openweather_dict["main"]["temp"])

def _parse_weather_type(openweather_dict: dict) -> WeatherType:
    try:
        weather_type_id = str(openweather_dict["weather"][0]["id"])
    except (IndexError, KeyError):
        raise ApiServiceError
    weather_types = {
        "200": WeatherType.Thunderstorm,
        "201": WeatherType.Thunderstorm,
        "202": WeatherType.Thunderstorm,
        "210": WeatherType.Thunderstorm,
        "211": WeatherType.Thunderstorm,
        "212": WeatherType.Thunderstorm,
        "221": WeatherType.Thunderstorm,
        "230": WeatherType.Thunderstorm,
        "231": WeatherType.Thunderstorm,
        "232": WeatherType.Thunderstorm,
        "300": WeatherType.Drizzle,
        "301": WeatherType.Drizzle,
        "302": WeatherType.Drizzle,
        "310": WeatherType.Drizzle,
        "311": WeatherType.Drizzle,
        "312": WeatherType.Drizzle,
        "313": WeatherType.Drizzle,
        "314": WeatherType.Drizzle,
        "321": WeatherType.Drizzle,
        "500": WeatherType.Rain,
        "501": WeatherType.Rain,
        "502": WeatherType.Rain,
        "503": WeatherType.Rain,
        "504": WeatherType.Rain,
        "511": WeatherType.Rain,
        "520": WeatherType.Rain,
        "521": WeatherType.Rain,
        "522": WeatherType.Rain,
        "531": WeatherType.Rain,
        "600": WeatherType.Snow,
        "601": WeatherType.Snow,
        "602": WeatherType.Snow,
        "611": WeatherType.Snow,
        "612": WeatherType.Snow,
        "613": WeatherType.Snow,
        "615": WeatherType.Snow,
        "616": WeatherType.Snow,
        "620": WeatherType.Snow,
        "621": WeatherType.Snow,
        "622": WeatherType.Snow,
        "701": WeatherType.Fog,
        "711": WeatherType.Fog,
        "721": WeatherType.Fog,
        "731": WeatherType.Fog,
        "741": WeatherType.Fog,
        "751": WeatherType.Fog,
        "761": WeatherType.Fog,
        "762": WeatherType.Fog,
        "771": WeatherType.Fog,
        "781": WeatherType.Fog,
        "800": WeatherType.Clear,
        "801": WeatherType.Clouds,
        "802": WeatherType.Clouds,
        "803": WeatherType.Clouds,
        "804": WeatherType.Clouds
    }
    for _id, _weather_type in weather_types.items():
        if weather_type_id.startswith(_id):
            return _weather_type
    raise ApiServiceError

def _parse_sun_time(
        openweather_dict: dict,
        time: Literal["sunrise"] | Literal["sunset"]) -> datetime:
    return datetime.fromtimestamp(openweather_dict["sys"][time])

def _parse_city(openweather_dict: dict) -> str:
    try:
        return openweather_dict["name"]
    except KeyError:
        raise ApiServiceError


if __name__ == "__main__":
    print(get_weather(Coordinates(latitude=55.7, longitude=37.6)))
