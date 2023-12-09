from fastapi import FastAPI
from routes.weather import weather_router


app = FastAPI()

app.include_router(weather_router, prefix="/api/weather", tags=["weather"])
