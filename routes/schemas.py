import datetime
from enum import Enum
from pydantic import BaseModel


class WeatherServicesEnum(Enum):
    TOMORROW_IO = "TOMORROW_IO"
    WEATHERBIT = "WEATHERBIT"


class NowInSchema(BaseModel):
    country: str
    city: str

    class Config:
        json_schema_extra = {
            "example": {
                "country": "Russia",
                "city": "Moscow",
            }
        }


class ForecastInSchema(BaseModel):
    country: str
    city: str
    when: datetime.datetime

    class Config:
        json_schema_extra = {
            "example": {
                "country": "Russia",
                "city": "Moscow",
                "when": "2023-12-05T23:55:19.947Z",
            }
        }


class OutSchema(BaseModel):
    temp_celsium: float
    is_precipitation: bool

    class Config:
        json_schema_extra = {
            "example": {"temp_celsium": "10", "is_precipitation": True}
        }
