from fastapi import FastAPI
from contextlib import asynccontextmanager
from datetime import datetime
import yaml
from app.services.weather import get_weather
from app.services.holidays import is_holiday
from app.services.maps import get_duration_minutes
from app.scheduler import start_scheduler

with open("config.yaml") as f:
    config = yaml.safe_load(f)

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = start_scheduler()
    yield
    scheduler.shutdown()

app = FastAPI(title="Traffic Predictor", lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "Traffic Predictor API is running"}

@app.get("/predict")
async def predict(origin: str, destination: str):
    city = config["city"]
    country = config["country"]
    now = datetime.now()

    duration = await get_duration_minutes(origin, destination)
    weather_data = await get_weather(f"{city},{country}")
    holiday = await is_holiday(country)

    factors = []
    adjusted = duration

    if "rain" in weather_data["weather"].lower():
        adjusted *= 1.20
        factors.append("lluvia detectada (+20%)")

    if now.weekday() == 4 and 17 <= now.hour <= 20:
        adjusted *= 1.15
        factors.append("viernes en hora punta (+15%)")
    elif now.weekday() < 5 and 7 <= now.hour <= 9:
        adjusted *= 1.10
        factors.append("hora punta matutina (+10%)")

    if holiday:
        factors.append("hoy es feriado — tráfico impredecible")

    adjusted = round(adjusted, 1)
    explanation = f"Google Maps estima {duration} min. " + (
        "Factores adicionales: " + ", ".join(factors) + f". Estimado ajustado: {adjusted} min."
        if factors else "No se detectaron factores adicionales."
    )

    return {
        "origin": origin,
        "destination": destination,
        "base_duration_minutes": duration,
        "adjusted_duration_minutes": adjusted,
        "weather": weather_data["weather"],
        "temperature": weather_data["temperature"],
        "is_holiday": holiday,
        "day_of_week": now.strftime("%A"),
        "explanation": explanation
    }