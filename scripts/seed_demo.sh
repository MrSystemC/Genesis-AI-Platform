#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
set -a
[ -f .env ] && . ./.env
set +a
. .venv/bin/activate
python scripts/seed_demo.py "$@"
