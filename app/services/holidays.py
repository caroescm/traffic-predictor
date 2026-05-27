import httpx
from datetime import date

async def is_holiday(country_code: str) -> bool:
    today = date.today()
    url = f"https://date.nager.at/api/v3/PublicHolidays/{today.year}/{country_code}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        holidays = response.json()
    
    today_str = today.strftime("%Y-%m-%d")
    return any(h["date"] == today_str for h in holidays)