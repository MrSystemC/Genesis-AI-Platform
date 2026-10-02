#!/usr/bin/env bash
set -euo pipefail
python - <<'PY'
import json, urllib.request
with urllib.request.urlopen('http://127.0.0.1:8000/api/v1/health',timeout=5) as r:
    data=json.load(r)
    assert data['status']=='ok', data
    print('OK', data)
PY
