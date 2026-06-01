# LumiSkin AI

LumiSkin AI is an MVP skincare analysis product with two local applications:

- `backend/`: FastAPI API for auth, uploads, questionnaires, OpenAI image analysis, and history.
- `app/`: React Native Expo mobile app.

The local workflow is intentionally simple: no Docker, no external database requirement, no S3, and no separate computer-vision process. The backend defaults to SQLite at `backend/preview.db` and local image storage under `backend/local_uploads/`.

## Quick Start

From the repository root:

```bash
bash start.sh
```

That starts:

- API: `http://localhost:8000`
- API health check: `http://localhost:8000/health`
- Expo dev server: `http://localhost:8081`

You can also start each side separately:

```bash
cd backend
bash start.sh
```

```bash
cd app
bash start.sh
```

## Backend

The backend is organized around thin routes, request controllers, SQLAlchemy models, and services:

- `api/`: FastAPI route declarations and dependencies.
- `controllers/`: request orchestration for route handlers.
- `models/`: database entities.
- `schemas/`: Pydantic request/response and OpenAI structured-output models.
- `services/`: local image storage, OpenAI analysis, auth, questionnaire, history, and recommendation logic.

`backend/start.sh` does the setup work:

- Creates `backend/.venv` if needed.
- Installs `backend/requirements.txt`.
- Creates `backend/.env` from `backend/.env.example` if needed.
- Initializes the local SQLite database.
- Starts the API on port `8000`.

The important backend environment variables are:

```env
ENVIRONMENT=local
DATABASE_URL=sqlite+pysqlite:///./preview.db
SECRET_KEY=change-me-use-a-long-random-secret-at-least-32-chars
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
```

Everything else has a local MVP default in `backend/core/config.py`.

Run backend tests:

```bash
cd backend
.venv/bin/python -m pytest
```

## OpenAI Analysis Flow

The mobile app uploads front, left, and right face photos to `/api/v1/uploads/images`. When it calls `/api/v1/analyses`, the backend reads the stored images, sends them to OpenAI as image inputs, and asks for a structured response matching `schemas/skin_analysis.py`.

The stored analysis includes:

- Objective concern scores for acne, redness, hyperpigmentation, fine lines, pores, oiliness, and dryness.
- Overall skin score and confidence.
- Primary concerns and objective summary.
- Routine steps.
- Korean skincare product recommendations.
- Dermatologist warning and cosmetic-use disclaimer.

## Local Auth Bypass

In development builds, the auth screens show `Skip login/signup`. It stores a fixed local-only token and sends you directly to the scan flow. The backend accepts that token only when `ENVIRONMENT=local`; production and preview environments still require normal auth.

## App

The Expo app lives in `app/`.

The local API URL is configured in `app/app.json`:

```json
{
  "apiBaseUrl": "http://localhost:8000/api/v1"
}
```

For a physical phone, replace `localhost` with your Mac's LAN IP address.

Expo Go on a physical phone cannot reach your Mac at `localhost`. Start the app with an explicit API URL:

```bash
cd app
EXPO_PUBLIC_API_BASE_URL=http://YOUR_MAC_LAN_IP:8000/api/v1 bash start.sh --lan
```

When using a LAN IP, start the backend on all interfaces:

```bash
cd backend
API_HOST=0.0.0.0 bash start.sh
```

Or use ngrok:

```bash
cd backend
bash start.sh
ngrok http 8000

cd ../app
EXPO_PUBLIC_API_BASE_URL=https://YOUR_NGROK_DOMAIN.ngrok-free.app/api/v1 bash start.sh --tunnel
```

Run app checks:

```bash
cd app
npm run typecheck
npx expo --version
```

## Useful Commands

```bash
# Start everything
bash start.sh

# Backend only
cd backend && bash start.sh

# App only
cd app && bash start.sh

# Backend tests
cd backend && .venv/bin/python -m pytest

# App typecheck
cd app && npm run typecheck
```
