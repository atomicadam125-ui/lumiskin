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
