#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
command -v python3 >/dev/null || { echo "Python 3.11+ is required"; exit 1; }
python3 - <<'PY'
import sys
if sys.version_info < (3, 11):
    raise SystemExit("Python 3.11+ is required")
PY
if [ ! -d .venv ]; then
  python3 -m venv .venv || { echo "Could not create venv. On Debian/Ubuntu install python3-venv and retry."; exit 1; }
fi
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
mkdir -p data
if [ ! -f .env ]; then
  SECRET="$(python - <<'PY'
import secrets
print(secrets.token_urlsafe(48))
PY
)"
  ADMIN_PASS="$(python - <<'PY'
import secrets,string
alphabet=string.ascii_letters+string.digits+'-_!@'
print('G!' + ''.join(secrets.choice(alphabet) for _ in range(18)) + '7')
PY
)"
  cat > .env <<EOF
GENESIS_ENV=development
GENESIS_SECRET_KEY=$SECRET
DATABASE_URL=sqlite:///./data/genesis.db
GENESIS_AUTORUN=1
GENESIS_TICK_INTERVAL_SECONDS=2
GENESIS_ALLOW_REGISTRATION=1
GENESIS_DEMO_MODE=1
GENESIS_TRUSTED_HOSTS=*
GENESIS_ADMIN_EMAIL=admin@genesis.local
GENESIS_ADMIN_PASSWORD=$ADMIN_PASS
EOF
  printf '\nAdmin account created for first launch:\n  email: admin@genesis.local\n  password: %s\n\nChange these values in .env before public deployment.\n' "$ADMIN_PASS"
fi
printf 'Genesis dependencies installed. Start with: ./scripts/start.sh\n'
