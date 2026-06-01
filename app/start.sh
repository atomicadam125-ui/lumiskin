#!/usr/bin/env bash
set -euo pipefail

# Local Expo app starter for MVP testing.
#
# Run from this folder:
#   bash start.sh
#
# What it does:
#   1. Verifies Node and npm are installed.
#   2. Installs npm dependencies when node_modules is missing.
#   3. Verifies Expo is available through npx.
#   4. Starts the Expo development server.
#
# Pass Expo arguments through after the script name:
#   bash start.sh --web
#   bash start.sh --ios
#
# For Expo Go on a physical phone, localhost points to the phone, not your Mac.
# Point the app at your backend with one of these:
#   EXPO_PUBLIC_API_BASE_URL=http://YOUR_MAC_LAN_IP:8000/api/v1 bash start.sh --lan
#   EXPO_PUBLIC_API_BASE_URL=https://YOUR_NGROK_DOMAIN.ngrok-free.app/api/v1 bash start.sh --tunnel

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if ! command -v node >/dev/null 2>&1; then
  echo "Node.js is required. Install the current LTS release and retry." >&2
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "npm is required. Install Node.js with npm and retry." >&2
  exit 1
fi

if [ ! -d node_modules ]; then
  npm install
fi

npx expo --version >/dev/null
npx expo start "$@"
