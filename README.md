# LumiSkin AI

LumiSkin AI is an MVP skincare analysis product with two local applications:

- `backend/`: FastAPI API plus the computer-vision service.
- `app/`: React Native Expo mobile app.

The local workflow is intentionally simple: no Docker, no external database requirement, and no extra process manager. The backend defaults to SQLite at `backend/preview.db` so a fresh laptop can run the project quickly.

## Quick Start

From the repository root:

```bash
bash start.sh
```

That starts:

- API: `http://localhost:8000`
- API health check: `http://localhost:8000/health`
- Computer vision service: `http://localhost:8010`
- CV health check: `http://localhost:8010/health`
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

Pass Expo flags through the app script:

```bash
cd app
bash start.sh --web
bash start.sh --ios
bash start.sh --android
```

## New Laptop Setup

The shell profile has aliases so `python` and `pip` resolve to Python 3:

```bash
alias python="python3"
alias pip="pip3"
```

Required local tools:

- Python 3.12+
- Node.js and npm
- Expo runs through `npx expo`, so no global Expo install is required.

## Backend

The backend lives in `backend/` and contains:

- `main.py`: FastAPI API entrypoint.
- `api/`: API routes and dependencies.
- `models/`, `schemas/`, `services/`, `db/`, `core/`: backend domain layers.
- `cv_service/`: separate FastAPI service for image analysis.
- `tests/`: backend test suite.
- `start.sh`: local backend startup script.

`backend/start.sh` does the setup work systematically:

- Creates `backend/.venv` if needed.
- Installs `backend/requirements.txt`.
- Creates `backend/.env` from `backend/.env.example` if needed.
- Initializes the local SQLite database.
- Starts the API on port `8000`.
- Starts the CV service on port `8010`.

Configuration is in `backend/.env`. The MVP default uses:

```env
DATABASE_URL=sqlite+pysqlite:///./preview.db
STORAGE_BACKEND=local
LOCAL_UPLOAD_DIR=local_uploads
```

Run backend tests:

```bash
cd backend
.venv/bin/python -m pytest
```

## App

The Expo app lives in `app/` and contains:

- `app/app/`: Expo Router screens.
- `app/src/api/`: API clients for auth and skincare flows.
- `app/src/components/`: reusable UI components.
- `app/src/store/`: Zustand stores.
- `app/start.sh`: local Expo startup script.

`app/start.sh` checks Node/npm, installs dependencies when `node_modules` is missing, verifies Expo through `npx`, and starts the Expo dev server.

The local API URLs are configured in `app/app.json`:

```json
{
  "apiBaseUrl": "http://localhost:8000/api/v1",
  "cvBaseUrl": "http://localhost:8010/v1"
}
```

For a physical phone, replace `localhost` with your Mac's LAN IP address.

Run app checks:

```bash
cd app
npm run typecheck
npx expo --version
```

## Product Flow

The mobile flow supports:

- Email/password registration and login.
- Native Sign in with Apple wiring for iOS.
- Front, left, and right skincare photo capture/upload.
- Questionnaire capture.
- Computer-vision scoring.
- Recommendation generation.
- Progress/history views.
- Account deletion.

The recommendation output is display-oriented and includes skin snapshot, scores, tier, improvement potential, routine steps, product cards, warnings, and a non-medical disclaimer.

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
