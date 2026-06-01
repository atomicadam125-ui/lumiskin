#!/usr/bin/env bash
set -euo pipefail

# Local backend starter for MVP testing.
#
# Run from this folder:
#   bash start.sh
#
# What it does:
#   1. Verifies Python is available as python3.
#   2. Creates backend/.venv when it does not exist.
#   3. Installs backend and computer-vision dependencies.
#   4. Copies .env.example to .env when needed.
#   5. Initializes the local SQLite database when DATABASE_URL uses sqlite.
#   6. Starts the API on :8000 and the CV service on :8010.
#
# Override ports when needed:
#   API_PORT=8002 CV_PORT=8012 bash start.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

API_HOST="${API_HOST:-127.0.0.1}"
API_PORT="${API_PORT:-8000}"
CV_HOST="${CV_HOST:-127.0.0.1}"
CV_PORT="${CV_PORT:-8010}"
VENV_DIR="$ROOT_DIR/.venv"
VENV_PYTHON="$VENV_DIR/bin/python"
RELOAD_ARG=""
export MPLCONFIGDIR="${MPLCONFIGDIR:-$ROOT_DIR/.cache/matplotlib}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required. Install Python 3.12+ and retry." >&2
  exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi

mkdir -p "$MPLCONFIGDIR"

"$VENV_PYTHON" -m pip install --quiet --disable-pip-version-check -r requirements.txt

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created backend/.env from backend/.env.example."
fi

"$VENV_PYTHON" scripts/init_local_db.py

if [ "${BACKEND_RELOAD:-false}" = "true" ]; then
  RELOAD_ARG="--reload"
fi

cleanup() {
  local pids
  pids="$(jobs -p)"
  if [ -n "$pids" ]; then
    kill $pids 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

echo "Starting skincare API at http://localhost:${API_PORT}"
"$VENV_PYTHON" -m uvicorn main:app --host "$API_HOST" --port "$API_PORT" $RELOAD_ARG &

echo "Starting CV service at http://localhost:${CV_PORT}"
"$VENV_PYTHON" -m uvicorn cv_service.main:app --host "$CV_HOST" --port "$CV_PORT" $RELOAD_ARG &

wait
