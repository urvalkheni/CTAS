# CTAS - Coastal Threat Alert System

A coastal monitoring workspace with a lightweight Next.js portal at the root and a larger React, Express, and FastAPI stack in `HackOut` for alerts, reports, weather, satellite maps, and coastal risk analysis.

## Overview

CTAS is a prototype for tracking coastal conditions and organizing community observations. The root app provides a simple web portal with dashboard pages and sample API routes. The `HackOut` workspace adds an interactive monitoring dashboard, backend services, and AI model endpoints. Together, they show how alerts, weather data, reports, map views, and prediction services can fit into one system.

## Features

- Root portal pages for Dashboard, Alerts, Reports, Leaderboard, Trends, About, and Settings.
- Mock Next.js API routes for auth, alerts, reports, and leaderboard data.
- MongoDB support through a cached connection helper and Mongoose models for users, reports, and alerts.
- `HackOut` React app with landing, login/register, protected dashboard, logout, weather, satellite, threat monitoring, community reports, analytics, and profile views.
- `HackOut` Express API for health, auth, weather, NOAA/current data, satellite, reports, threats, users, and community reports.
- FastAPI AI service with model status, coastal threat prediction, mangrove health, algal bloom, ensemble scoring, and model retraining endpoints.
- Map-based visualization using Google Maps and Leaflet components.
- Community reporting workflows with report creation, filtering, status changes, SMS alert helpers, and nearby-report endpoints.

## Tech Stack

- Languages: TypeScript, JavaScript, Python.
- Root frontend: Next.js 15, React 19, Tailwind CSS 4, Mongoose, bcryptjs, Leaflet, React Leaflet, Recharts.
- `HackOut` frontend: React 18, Vite, React Router, Redux Toolkit, Axios, Lucide React, React Hot Toast, Tailwind CSS 3, Framer Motion, Leaflet, React Leaflet, Recharts.
- `HackOut` backend: Node.js, Express, Mongoose, JWT, bcryptjs, CORS, Helmet, Morgan, Compression, Multer, Nodemailer, Twilio, ws, xml2js.
- AI service: FastAPI, Uvicorn, Pydantic, NumPy, Pandas, Scikit-learn, TensorFlow, PyTorch, GeoPandas, Rasterio, OpenCV, Matplotlib, Folium.
- Tools and deployment: npm, Vercel, Railway, Docker Compose, PowerShell-friendly setup scripts.

## Project Structure

- `app/` -> Active Next.js route tree and API handlers for the root portal.
- `src/app/` -> Default starter files kept in the repo; the live app uses `app/`.
- `lib/mongodb.ts` -> Cached MongoDB connection helper for the root app.
- `models/` -> Mongoose schemas for users, reports, and alerts.
- `public/` -> Static assets used by the root app.
- `HackOut/frontend/` -> React/Vite dashboard, routing, Redux store, UI components, and local services.
- `HackOut/backend/` -> Express server, controllers, routes, middleware, and database setup.
- `HackOut/ai-models/` -> Python model scripts and the FastAPI prediction service.
- `HackOut/Dataset_for_chatbot.csv` -> Dataset used by the workspace chatbot utilities.
- `HackOut/deploy*.sh`, `HackOut/deploy*.bat`, `HackOut/docker-compose.yml`, `HackOut/vercel.json`, `HackOut/railway.json` -> Deployment helpers and platform configuration.
- `components/` and `styles/` -> Empty root-level placeholders in the current workspace.

## Setup & Installation

Run each service in its own terminal. If you only want the root portal, stop after step 2.

1. Clone the repository.

```bash
git clone <repo-url>
cd CTAS
```

This downloads the project and moves you into the repository root.

2. Install and start the root Next.js portal.

```bash
npm install
npm run dev
```

This installs the root dependencies and starts the Next.js app on `http://localhost:3000`.

3. Create the `HackOut` environment file if you want to run the extended stack.

```powershell
Copy-Item HackOut\.env.example HackOut\.env
```

Edit `HackOut\.env` and fill in `MONGODB_URI`, `JWT_SECRET`, and any API keys before starting the backend.

4. Start the `HackOut` frontend.

```bash
cd HackOut\frontend
npm install
npm run dev
```

This starts the Vite app on `http://localhost:5173`.

5. Start the `HackOut` backend.

```bash
cd HackOut\backend
npm install
npm run dev
```

This starts the Express API on `http://localhost:5000`.

6. Start the AI model service.

```bash
cd HackOut\ai-models
python -m pip install -r requirements.txt
python api/main.py
```

This installs the Python dependencies and starts the FastAPI service on `http://localhost:8000`.

## Usage Examples

```bash
npm run dev
```

Starts the root portal so you can open the dashboard, alerts, reports, and other Next.js pages.

```bash
curl http://localhost:5000/api/health
```

Checks that the `HackOut` backend is running.

```bash
curl http://localhost:8000/models/status
```

Checks which AI models are available in the FastAPI service.

```bash
curl http://localhost:3000/api/alerts
```

Returns the sample alert payload used by the root Next.js app.

## Example Output

```json
{
    "status": "OK",
    "message": "CTAS Backend API is running",
    "timestamp": "2026-04-09T12:00:00.000Z",
    "version": "1.0.0"
}
```

```json
{
    "models": {
        "algal_bloom": { "status": "ready" },
        "sea_level": { "status": "unavailable" },
        "cyclone": { "status": "ready" }
    }
}
```

These responses show the backend health check and the AI model service status format.

## How It Works

1. The root Next.js app renders the coastal portal and serves mock JSON endpoints.
2. The `HackOut` frontend stores auth data in `localStorage`, routes with React Router, and shows dashboard modules based on the selected view.
3. The frontend calls the Express backend for weather, NOAA, satellite, report, auth, and community-report data.
4. The backend reads environment variables, connects to MongoDB, and returns route-specific JSON.
5. The FastAPI service loads any available AI model classes and returns prediction or status payloads.

## Limitations / Notes

- Several root API routes return mock data instead of writing to a database.
- Some `HackOut` UI modules rely on services or API keys that must be configured in `.env`.
- AI model loading is optional; missing model files are reported as unavailable rather than crashing the service.
- The repository includes starter files and experimental components that are not part of the active root app route tree.
- The satellite component loads Google Maps from an external script, so it requires network access and a valid key.

## Learning Outcomes

- Next.js app routing and API handlers.
- React state management with Redux and React Router.
- MongoDB and Mongoose schema design.
- Express API development.
- FastAPI and Pydantic service design.
- External API integration for weather and NOAA data.
- Map-based UI and geospatial visualization.
- Basic ML-serving patterns.

## Future Improvements

- Replace mock root endpoints with persistent database-backed handlers.
- Unify the root Next.js portal and `HackOut` UI into one cohesive frontend.
- Add automated tests for the backend and AI service.
- Persist report and alert creation instead of relying on sample data in the root app.

## Disclaimer

This repository is a prototype and demo workspace. It should not be treated as an emergency-warning system or as an authoritative environmental forecast source.

