from dataclasses import dataclass
import requests
from exceptions import CantGetCoordinates

@dataclass
class Coordinates:
    longitude: float
    latitude: float

def get_gps_coordinates() -> Coordinates:
    """Returns current coordinates using our GPS"""
    # Выполняем запрос к сервису для получения координат
    response = requests.get("https://ipinfo.io/json")
    
    # Проверяем, успешен ли запрос
    if response.status_code == 200:
        data = response.json()
        loc = data.get("loc", "")
        
        if loc:
            latitude, longitude = loc.split(",")
            return Coordinates(longitude=float(longitude), latitude=float(latitude))  # Исправлено порядок
        else:
            raise CantGetCoordinates("Location data not found.")
    else:
        raise CantGetCoordinates(f"Request failed with status code: {response.status_code}")

if __name__ == "__main__":  # Исправлено
    try:
        print(get_gps_coordinates())
    except CantGetCoordinates as e:
        print(f"Error: {e}")

        




