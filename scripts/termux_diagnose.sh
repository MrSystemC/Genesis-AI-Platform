#!/data/data/com.termux/files/usr/bin/bash
set -e
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
. .venv/bin/activate
python - <<'PY'
checks=['fastapi','uvicorn','pydantic','sqlalchemy']
print('Genesis Environment Check')
for c in checks:
    try:
        __import__(c)
        print('[OK]', c)
    except Exception as e:
        print('[FAIL]', c, e)
PY
