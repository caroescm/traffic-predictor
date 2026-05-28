# Product Requirements Document (PRD)
## Traffic Predictor

---

## 1. Problem Statement

Apps like Google Maps provide ETAs that are technically accurate at a global scale, but frequently imprecise in cities with complex traffic dynamics or informal public transport systems. The underlying issue is not that Google Maps ignores relevant factors — it does model time of day, historical patterns, and transport type — but that its models are trained globally and cannot fully capture hyperlocal conditions.

In cities like Lima, Peru, factors such as heavy rainfall, local public holidays, and neighborhood-specific congestion patterns can add 20–50% to a predicted travel time. Users who rely on the app's ETA as-is consistently arrive late, despite having planned ahead.

**Traffic Predictor does not replace Google Maps.** It acts as a local intelligence layer on top of it — enriching the base ETA with real-time weather, local holiday data, and city-specific historical patterns to give users a more reliable departure time recommendation.

---

## 2. Objective

Build an open-source, self-hostable web app that takes a Google Maps ETA and adjusts it based on local context, giving users a more accurate answer to: *"When should I actually leave?"*

---

## 3. Target Users

### 3.1 Frequent Commuter
A person who travels regularly through the city — typically for work — and needs to know how far in advance to leave, especially on routes they know well but where conditions vary significantly by day and time.

**Core need:** Reliable departure time, not just distance or nominal ETA.

### 3.2 Visitor / Tourist
Someone unfamiliar with the city's traffic patterns who needs guidance they cannot derive from personal experience. A tourist doesn't know that Friday afternoon in Miraflores is categorically different from Tuesday morning.

**Core need:** Trustworthy ETA in an unfamiliar environment.

### 3.3 Researcher / Developer
A technical user interested in urban mobility data. Traffic Predictor generates a structured historical dataset of travel times, weather conditions, and holiday flags over time — useful for independent analysis or integration into other tools.

**Core need:** Access to clean, local mobility data via API.

---

## 4. Product Overview

Traffic Predictor is a FastAPI-based backend that:

1. Queries the **Google Maps Directions API** for a base ETA between an origin and destination
2. Fetches **current weather conditions** from OpenWeatherMap
3. Checks whether today is a **local public holiday** using the Nager.Date API
4. Queries its own **PostgreSQL database** for historical travel time patterns on similar days and conditions
5. Returns an **adjusted ETA** with a plain-language explanation of the factors that influenced it

The app is configurable via `config.yaml` for any city. Initial deployment targets **Lima, Peru**.

---

## 5. Features

### 5.1 Base ETA Retrieval
Query the Google Maps Directions API for a real-time route duration between any origin and destination within the configured city.

### 5.2 Weather Enrichment
Fetch current weather conditions (description + temperature) from OpenWeatherMap and factor them into the adjusted ETA. Rain and extreme heat are known to increase travel times in Lima.

### 5.3 Holiday Detection
Check whether the current date is a local public holiday using Nager.Date (free, no API key required). Holidays affect traffic in non-obvious ways — some routes get worse, others get better.

### 5.4 Historical Pattern Matching
Query the app's own database for past travel times on the same route, same day of the week, and similar time of day. As the app accumulates data, this becomes its most powerful feature.

### 5.5 Adjusted ETA + Explanation
Return a recommended departure time and a short explanation, e.g.:  
*"Google Maps says 40 min. Today is rainy and it's Friday afternoon — historically this route takes ~25% longer under these conditions. We recommend leaving 50 min early."*

### 5.6 Data Collection (Background Scheduler)
An APScheduler job runs at regular intervals to query and store travel times for configured seed routes. This builds the historical dataset over time.

### 5.7 REST API
All features are exposed via a documented REST API (FastAPI + Swagger UI at `/docs`). Researchers and developers can query the API or access historical data programmatically.

---

## 6. Out of Scope (v1.0)

The following are explicitly not part of the first version:

- **Turn-by-turn navigation** — Traffic Predictor does not provide routing
- **Real-time traffic incident alerts** — no integration with Waze or similar
- **Mobile app** — v1 is a web API and basic HTML frontend only
- **User accounts / authentication** — no login system in v1
- **Multiple simultaneous cities** — one city per deployment instance

---

## 7. Success Metrics

| Metric | Goal |
|---|---|
| Adjusted ETA accuracy | Within 10% of actual travel time in 70%+ of cases (after 30 days of data) |
| Data collection uptime | Scheduler runs successfully 95%+ of the time |
| API response time | Under 3 seconds per request |
| Open source adoption | At least 3 cities successfully configure and run their own instance |

---

## 8. Risks & Limitations

### 8.1 Cold Start Problem
Traffic Predictor's historical pattern matching requires data to be useful. On day one, the app has no history. The adjusted ETA will be based only on weather and holiday data until enough historical records are accumulated.

**Mitigation:** Be transparent with the user about data age. Show how many historical data points were used in the estimate.

### 8.2 Google Maps API Cost
The Directions API is not free at scale. Heavy usage can incur costs.

**Mitigation:** Cache repeated queries. Limit seed routes to high-value corridors. Document free tier limits clearly in the README.

### 8.3 Weather Data Accuracy
OpenWeatherMap's free tier updates every 10 minutes and may lag real conditions.

**Mitigation:** Acceptable for v1. Can be upgraded to a paid tier or alternative source in future versions.

### 8.4 Holiday Data Coverage
Nager.Date covers national public holidays but may miss regional or informal holidays (e.g., regional strikes, local festivities) that also affect traffic.

**Mitigation:** Allow manual holiday overrides via `config.yaml` in a future version.

---

## 9. Technical Stack

| Component | Technology |
|---|---|
| Backend framework | FastAPI (Python) |
| Database | PostgreSQL (local) |
| ORM | SQLAlchemy |
| Background scheduler | APScheduler |
| HTTP client | httpx |
| Config management | PyYAML + python-dotenv |
| External APIs | Google Maps Directions, OpenWeatherMap, Nager.Date |

---

## 10. Open Source Principles

Traffic Predictor is designed to be easy to install and run by anyone:

- All dependencies are listed in `requirements.txt`
- City configuration is isolated in `config.yaml` — no code changes needed to deploy for a new city
- No proprietary services required (PostgreSQL runs locally)
- API keys are stored in `.env` and never committed to version control
- Full setup instructions will be documented in `README.md`

---

*This document will be updated as the project evolves.*
