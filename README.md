# ColdGuard Backend

Backend for the ColdGuard pharmaceutical cold chain monitoring system. It exposes a REST API for user and device management, an MQTT bridge for ESP32 hardware control, and an MCP endpoint that connects an AI agent (ASHA) to the frontend client.

## What it does

ColdGuard monitors cold storage units used in low-resource healthcare settings (targeted at West Africa). IoT sensors on an ESP32 record temperature, humidity, and light intensity. The backend:

1. Stores sensor readings in MongoDB.
2. Exposes them to an AI research agent that applies the Arrhenius degradation equation and cross-references WHO/USP pharmaceutical storage guidelines to produce a drug viability verdict: **SAFE**, **MONITOR**, or **DO NOT USE**.
3. Lets users control physical devices (LEDs, buzzers, motors) through natural language via the ASHA MCP agent.
4. Supports scheduled automations (e.g. "turn on the light every morning at 6am") stored as cron workflows in MongoDB.

## Architecture

```
Frontend (AI client)
    │
    ├── REST API  (/api/v1/...)        ← user auth, projects, device registry, sensor ingestion
    │
    └── MCP endpoint (/mcp)           ← ASHA agent tools (hardware control + drug reports)
            │
            ├── MQTT broker           ← publishes commands to ESP32 microcontrollers
            │
            └── Qwen AI (Alibaba)     ← research agent: sensor analysis + web search
```

## Tech stack

| Layer | Technology |
|---|---|
| Framework | FastAPI + Uvicorn |
| Database | MongoDB via Motor + Beanie ODM |
| Auth | JWT (python-jose), PBKDF2-SHA256 password hashing |
| IoT | paho-mqtt (MQTT broker bridge) |
| AI agent | FastMCP, OpenAI-compatible SDK pointed at Qwen on Alibaba MaaS |
| Scheduler | APScheduler (jobs stored in MongoDB) |
| Rate limiting | slowapi |

## API routes

All routes under `/api/v1/` require a Bearer JWT except where marked public.

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/users/create` | public | Register a new user |
| POST | `/api/v1/users/login` | public | Login, returns JWT |
| POST | `/api/v1/projects/create_project` | user | Create a cold storage project (generates ASHA ID) |
| GET | `/api/v1/projects/get_all_projects` | admin | List all projects |
| POST | `/api/v1/asha/verify_and_register_device` | public | Register an ESP32 device against a valid ASHA ID |
| POST | `/api/v1/asha/get_all_devices_for_project_by_logged_in_user` | user | Get devices owned by current user |
| POST | `/api/v1/asha/get_project_and_devices` | user | Get projects + device details for current user |
| POST | `/api/v1/sensor/add_data` | public | Ingest sensor readings from hardware |

## MCP tools (ASHA agent)

The MCP endpoint at `/mcp` is consumed by the frontend AI client. Available tools:

- **`get_sensor_data(days)`** — fetches historical temperature/humidity/light readings (max 14 days).
- **`build_vaccine_report(days, prompt)`** — runs the Qwen research agent over sensor data and returns a full pharmaceutical viability report with potency estimate, verdict, reasoning, and recommended action.

## Data models

- **User** — email (unique), name, hashed password.
- **Project** — name, `AshaID` (unique UUID, acts as device token), created by user.
- **AshaDevice** — maps an `auth_id` (same as `AshaID`) to a list of physical device pins and their bus types.
- **Sensor** — timestamp, temperature (°C), humidity (%), light intensity.
- **Workflow** — cron expression + list of MQTT payloads for scheduled automations.

## Environment variables

Copy `.env.example` to `.env` and fill in all values.

```
MONGO_URL=                    # MongoDB connection string
FRONTEND_URL=                 # CORS allowed origin
JWT_SECRET_KEY=               # Strong random secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ENV=development               # set to "production" to disable /docs
ADMIN_IDS=                    # Comma-separated MongoDB ObjectIds for admin users
QWEN_API_KEY=                 # Alibaba MaaS API key for the research agent
MAAT_ENDPOINT=                # Internal service endpoint
MQTT_IP=                      # MQTT broker host
MQTT_PORT=                    # MQTT broker port
```

## Running locally

```bash
uv sync
uv run python main.py
```

The MCP agent can also be run standalone (without the REST API) for development:

```bash
uv run python mcp_main.py
```

## Known limitations

- Sensor readings are stored in a single global collection with no device or project association. All users share the same sensor pool. This is intentional for the current single-device deployment but will need a `device_id` field added before supporting multiple devices.
- The MCP endpoint has no authentication at the transport layer — access control is delegated to the frontend client.
