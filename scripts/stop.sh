#!/usr/bin/env bash
set -euo pipefail
pkill -f "uvicorn genesis.app:app" 2>/dev/null || true
