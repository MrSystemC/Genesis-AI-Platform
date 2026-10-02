#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
set -a
[ -f .env ] && . ./.env
set +a
. .venv/bin/activate
exec uvicorn genesis.app:app --host 0.0.0.0 --port "${PORT:-8000}"
