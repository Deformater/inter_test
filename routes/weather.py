from fastapi import APIRouter, HTTPException
from routes.exceptions import (
    AddressNotFound,
    ServiceUnavailable,
    AllServicesUnavailable,
)
from routes.schemas import NowInSchema, ForecastInSchema, OutSchema
from routes.external_api_service import WeatherAPIService, MapAPIService


weather_router = APIRouter()


@weather_router.post("/now/", status_code=200, response_model=OutSchema)
def post_now(body: NowInSchema):
    """
    Endpoint to get the current weather for a given city and country.
    """
    try:
        cords = MapAPIService(body.city, body.country).get_cords()
        weather = WeatherAPIService(cords).get_weather_now()
        return weather
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except AddressNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (ServiceUnavailable, AllServicesUnavailable) as e:
        raise HTTPException(status_code=503, detail=str(e))


@weather_router.post("/forecast/", status_code=200, response_model=OutSchema)
def post_forecast(body: ForecastInSchema):
    """
    Endpoint to get up to 5 days weather forecast for a specific city and country.
    """
    try:
        cords = MapAPIService(body.city, body.country).get_cords()
        weather = WeatherAPIService(cords, body.when).get_weather_forecast()
        return weather
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except AddressNotFound as e:
        raise HTTPException(status_code=404, detail=str(e))
    except (ServiceUnavailable, AllServicesUnavailable) as e:
        raise HTTPException(status_code=503, detail=str(e))
