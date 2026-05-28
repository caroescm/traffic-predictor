# Traffic Predictor

A self-hostable web app that enriches Google Maps ETAs with local context — weather, public holidays, and historical patterns — to give you a more accurate answer to: **"When should I actually leave?"**

Built for cities where global navigation apps consistently underestimate travel time due to hyperlocal conditions. Initial deployment targets **Lima, Peru**.

---

## How it works

1. You enter an origin and destination
2. The app queries the **Google Maps Routes API** for a base ETA
3. It fetches **current weather** from OpenWeatherMap
4. It checks whether today is a **public holiday** via Nager.Date
5. It applies local adjustment factors and returns an **adjusted ETA** with a plain-language explanation

A background scheduler also collects travel time data every 30 minutes on configured seed routes, building a historical dataset over time.

---

## Features

- Adjusted ETA based on weather, day of week, and holidays
- Plain-language explanation of factors that influenced the estimate
- Background data collector (APScheduler) for building historical patterns
- REST API with auto-generated docs at `/docs`
- Configurable for any city via `config.yaml`

---

## Tech stack

| Component | Technology |
|---|---|
| Backend | FastAPI (Python) |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Scheduler | APScheduler |
| HTTP client | httpx |
| Config | PyYAML + python-dotenv |
| External APIs | Google Maps Routes, OpenWeatherMap, Nager.Date |

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/traffic-predictor.git
cd traffic-predictor
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Create a `.env` file

```
DATABASE_URL=postgresql://localhost/traffic_predictor
OPENWEATHER_API_KEY=your_openweathermap_key
GOOGLE_MAPS_API_KEY=your_google_maps_key
```

- **OpenWeatherMap**: Free API key at [openweathermap.org](https://openweathermap.org/api)
- **Google Maps Routes API**: Enable at [Google Cloud Console](https://console.cloud.google.com). Note: requires billing to be enabled, but stays within the free tier for low usage.

### 4. Create the database

```bash
createdb traffic_predictor
python3 -c "from app.database import Base, engine; from app.models import TravelQuery; Base.metadata.create_all(bind=engine)"
```

### 5. Configure your city

Edit `config.yaml`:

```yaml
city: "Lima"
country: "PE"
timezone: "America/Lima"
seed_routes:
  - name: "Miraflores a San Isidro"
    origin: "Miraflores, Lima, Peru"
    destination: "San Isidro, Lima, Peru"
```

Change `city`, `country` (ISO 3166-1 alpha-2 code), `timezone`, and `seed_routes` for your city.

### 6. Run the app

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/static/index.html` in your browser.

API docs available at `http://127.0.0.1:8000/docs`.

---

## API

### `GET /predict`

Returns an adjusted ETA for a given origin and destination.

**Parameters:**
- `origin` — starting address (string)
- `destination` — destination address (string)

**Example:**
```
GET /predict?origin=Miraflores,Lima,Peru&destination=San%20Isidro,Lima,Peru
```

**Response:**
```json
{
  "origin": "Miraflores,Lima,Peru",
  "destination": "San Isidro,Lima,Peru",
  "base_duration_minutes": 14.3,
  "adjusted_duration_minutes": 17.2,
  "weather": "light rain",
  "temperature": 19.5,
  "is_holiday": false,
  "day_of_week": "Friday",
  "explanation": "Google Maps estima 14.3 min. Factores adicionales: lluvia detectada (+20%). Estimado ajustado: 17.2 min."
}
```

---

## Notes

- On day one, the app has no historical data. Adjusted ETAs are based only on weather and holiday information until the scheduler accumulates records.
- Google Maps Routes API has a free tier — see [pricing](https://developers.google.com/maps/documentation/routes/usage-and-billing) before running at high frequency.
- The scheduler runs every 30 minutes by default. You can change the interval in `app/scheduler.py`.

---

*Contributions welcome. To deploy for a new city, only `config.yaml` needs to change — no code modifications required.*
