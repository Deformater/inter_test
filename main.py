from fastapi import FastAPI
from routes.weather import router


app = FastAPI()

app.include_router(router, prefix="/api/weather", tags=["weather"])
