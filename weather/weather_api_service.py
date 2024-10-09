from dataclasses import dataclass
from datetime import datetime
from typing import TypeAlias
from enum import Enum

from coordinates import Coordinates

class WeatherType(Enum):
    Thunderstorm = "Гроза"
    Drizzle = "Изморось"
    Snow = "Снег"
    Clear = "Ясно"
    Fog = "Туман"
    Clouds = "Облачно"
    

Celsius: TypeAlias = int

@dataclass
class Weather:
    temperature: Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime
    city: str

def get_weather(coordinates: Coordinates) -> Weather:
    """Request weather in OpenWeather API and returns it"""
    return Weather(
            temperature=20,
            weather_type=WeatherType.Clear,
            sunrise=datetime.fromisoformat("2022-05-04 04:00:00"),
            sunset=datetime.fromisoformat("2022-05-04 20:25:00"),
            city="Moscow"
            )
    


