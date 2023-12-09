from fastapi import APIRouter, HTTPException
from routes.exceptions import (
    AddressNotFound,
    ServiceUnavailable,
    AllServicesUnavailable,
)
from routes.schemas import InNow, OutNow
from routes.external_api_service import WeatherAPIService, MapAPIService


weather_router = APIRouter()


@weather_router.post("/now/", status_code=200, response_model=OutNow)
def post_now(body: InNow):
    try:
        cords = MapAPIService(body.city, body.country).get_cords()
        weather = WeatherAPIService(cords, body.when).get_weather_now()
        return weather
    except AddressNotFound as e:
        raise HTTPException(status_code=404, detail=e)
    except (ServiceUnavailable, AllServicesUnavailable) as e:
        raise HTTPException(status_code=503, detail=e)


@weather_router.post("/forecast/", status_code=200, response_model=OutNow)
def post_forecast(body: InNow):
    try:
        cords = MapAPIService(body.city, body.country).get_cords()
        weather = WeatherAPIService(cords, body.when).get_weather_forecast()
        return weather
    except AddressNotFound as e:
        raise HTTPException(status_code=404, detail=e)
    except (ServiceUnavailable, AllServicesUnavailable) as e:
        raise HTTPException(status_code=503, detail=e)
