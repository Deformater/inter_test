import datetime
import requests
from settings import Settings
from routes.exceptions import (
    AddressNotFound,
    ServiceUnavailable,
    AllServicesUnavailable,
)
from routes.schemas import WeatherServicesEnum, OutNow


class WeatherAPIService:
    API_KEYS = {
        WeatherServicesEnum.TOMORROW_IO: Settings.TOMORROW_IO_API_KEY,
        WeatherServicesEnum.WEATHERBIT: "Settings.WEATHERBIT_API_KEY",
        WeatherServicesEnum.OPENWEATHER: "Settings.OPENWEATHER_API_KEY",
    }
    BASE_URLS = {
        WeatherServicesEnum.TOMORROW_IO: Settings.TOMORROW_IO_API_BASE_URL,
        WeatherServicesEnum.WEATHERBIT: "Settings.WEATHERBIT_API_BASE_URL",
        WeatherServicesEnum.OPENWEATHER: "Settings.OPENWEATHER_API_BASE_URL",
    }
    LIMIT = 1

    def __init__(self, cords: list[float], when: datetime.datetime):
        self.cords = cords
        self.time = when

    def get_weather_forecast(self):
        for service in WeatherServicesEnum:
            try:
                return self.__get_forecast_weather_from_service(service)
            except ServiceUnavailable:
                continue
        else:
            raise AllServicesUnavailable(self.API_KEYS.values())

    def __get_forecast_weather_from_service(self, service: WeatherServicesEnum):
        api_key = self.API_KEYS[service]
        base_url = self.BASE_URLS[service]

        match service:
            case WeatherServicesEnum.TOMORROW_IO:
                params = {
                    "apikey": api_key,
                    "location": f"{self.cords[0]}, {self.cords[1]}",
                    "timesteps": ["1d"],
                    "units": "metric",
                }
                response = requests.get(f"{base_url}weather/forecast", params=params)

                if response.status_code != 200:
                    raise ServiceUnavailable(base_url)

                for day_forecast in response.json()["timelines"]["daily"]:
                    if (
                        datetime.datetime.fromisoformat(day_forecast["time"]).date()
                        == self.time.date()
                    ):
                        temperature = day_forecast["values"]["temperatureAvg"]
                        is_precipitation = (
                            day_forecast["values"]["precipitationProbabilityAvg"] > 0
                        )
                        break

            case WeatherServicesEnum.WEATHERBIT:
                pass
            case WeatherServicesEnum.OPENWEATHER:
                pass
            case _:
                raise ValueError(f"Unknown service: {service}")
        return OutNow(temp_celsium=temperature, is_precipitation=is_precipitation)

    def get_weather_now(self):
        for service in WeatherServicesEnum:
            try:
                return self.__get_now_weather_from_service(service)
            except ServiceUnavailable:
                continue
        else:
            raise AllServicesUnavailable(self.API_KEYS.values())

    def __get_now_weather_from_service(self, service: WeatherServicesEnum):
        api_key = self.API_KEYS[service]
        base_url = self.BASE_URLS[service]

        match service:
            case WeatherServicesEnum.TOMORROW_IO:
                params = {
                    "apikey": api_key,
                    "location": f"{self.cords[0]}, {self.cords[1]}",
                    "units": "metric",
                }
                response = requests.get(f"{base_url}weather/realtime", params=params)

                if response.status_code != 200:
                    raise ServiceUnavailable(base_url)

                data = response.json()["data"]
                temperature = data["values"]["temperature"]
                is_precipitation = data["values"]["precipitationProbability"] > 0

            case WeatherServicesEnum.WEATHERBIT:
                pass
            case WeatherServicesEnum.OPENWEATHER:
                pass
            case _:
                raise ValueError(f"Unknown service: {service}")
        return OutNow(temp_celsium=temperature, is_precipitation=is_precipitation)


class MapAPIService:
    API_KEY = Settings.YANDEX_MAP_API
    BASE_URL = Settings.YANDEX_MAP_API_BASE_URL
    LANG = "ru_RU"
    TYPE = "geo"
    LIMIT = 1

    def __init__(self, city: str, country: str) -> None:
        self.city = city
        self.country = country

    def get_cords(self) -> list[float]:
        params = {
            "apikey": self.API_KEY,
            "text": f"г. {self.city},{self.country}",
            "lang": self.LANG,
            "type": self.TYPE,
            "results": self.LIMIT,
        }

        try:
            response = requests.get(self.BASE_URL, params=params)
            if response.status_code != "200":
                raise ServiceUnavailable(self.BASE_URL)
            features = response.json()["features"]

            if not features:
                raise AddressNotFound(self.city, self.country)

            if features[0]["properties"]["GeocoderMetaData"]["kind"] != "locality":
                raise AddressNotFound(self.city, self.country)

            return features[0]["geometry"]["coordinates"]
        except (KeyError, IndexError):
            raise AddressNotFound(self.city, self.country)
