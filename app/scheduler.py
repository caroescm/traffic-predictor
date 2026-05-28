from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import yaml

from app.services.maps import get_duration_minutes
from app.services.weather import get_weather
from app.services.holidays import is_holiday
from app.database import SessionLocal
from app.models import TravelQuery

with open("config.yaml") as f:
    config = yaml.safe_load(f)

async def collect_data():
    db = SessionLocal()
    try:
        weather_data = await get_weather(f"{config['city']},{config['country']}")
        holiday = await is_holiday(config["country"])
        now = datetime.now()

        for route in config["seed_routes"]:
            duration = await get_duration_minutes(route["origin"], route["destination"])
            record = TravelQuery(
                city=config["city"],
                origin=route["origin"],
                destination=route["destination"],
                duration_minutes=duration,
                weather=weather_data["weather"],
                temperature=weather_data["temperature"],
                is_holiday=holiday,
                day_of_week=now.strftime("%A"),
                queried_at=now
            )
            db.add(record)
        db.commit()
        print(f"[{now}] Datos recolectados correctamente.")
    finally:
        db.close()

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(collect_data, "interval", minutes=30)
    scheduler.start()
    return scheduler