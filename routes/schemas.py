import datetime
from pydantic import BaseModel


class InNow(BaseModel):
    country: str
    city: str
    when: datetime.datetime

    class Config:
        schema_extra = {
            "example": {
                "contry": "Russia",
                "city": "Moscow",
                "when": "2023-12-05T23:55:19.947Z",
            }
        }


class OutNow(BaseModel):
    temp_celsium: str
    is_precipitation: bool

    class Config:
        schema_extra = {"example": {"temp_celsium": "10", "is_precipitation": True}}
