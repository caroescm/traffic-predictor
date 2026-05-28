import httpx
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

async def get_duration_minutes(origin: str, destination: str) -> float:
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_MAPS_API_KEY,
        "X-Goog-FieldMask": "routes.duration"
    }
    body = {
        "origin": {"address": origin},
        "destination": {"address": destination},
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=body)
        response.raise_for_status()
        data = response.json()

    duration_str = data["routes"][0]["duration"]
    duration_seconds = int(duration_str.replace("s", ""))
    return round(duration_seconds / 60, 1)