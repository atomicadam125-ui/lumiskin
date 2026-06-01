#!/usr/bin/env bash
set -euo pipefail

# Starts the full local MVP stack from the repository root:
#   bash start.sh
#
# This delegates setup to:
#   backend/start.sh  - FastAPI API plus CV service
#   app/start.sh      - Expo development server
#
# Expo arguments can be passed through:
#   bash start.sh --web

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cleanup() {
  local pids
  pids="$(jobs -p)"
  if [ -n "$pids" ]; then
    kill $pids 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

(cd "$ROOT_DIR/backend" && bash start.sh) &
BACKEND_PID=$!

sleep 3

(cd "$ROOT_DIR/app" && bash start.sh "$@") &
APP_PID=$!

wait "$BACKEND_PID" "$APP_PID"
