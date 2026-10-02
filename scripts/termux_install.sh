#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [ -z "${TERMUX_VERSION:-}" ] && [[ "${PREFIX:-}" != *"com.termux"* ]]; then
  echo "This installer is for Termux only."
  exit 1
fi

pkg update -y
pkg install -y python openssl libffi

PY_MAJOR=$(python - <<'PY'
import sys
print(f"{sys.version_info.major}.{sys.version_info.minor}")
PY
)

case "$PY_MAJOR" in
  3.11|3.12) echo "Python $PY_MAJOR OK" ;;
  *) echo "Unsupported Python $PY_MAJOR. Use Termux Python 3.11/3.12 for Genesis."; exit 1 ;;
esac

python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements-termux.txt

mkdir -p data

if [ ! -f .env ]; then
SECRET="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
ADMIN_PASS="$(python -c 'import secrets; print("G!"+secrets.token_urlsafe(16)+"7")')"
cat > .env <<ENV
GENESIS_ENV=termux
GENESIS_SECRET_KEY=$SECRET
DATABASE_URL=sqlite:///./data/genesis.db
GENESIS_AUTORUN=1
GENESIS_TICK_INTERVAL_SECONDS=2
GENESIS_ALLOW_REGISTRATION=1
GENESIS_DEMO_MODE=1
GENESIS_TRUSTED_HOSTS=*
GENESIS_ADMIN_EMAIL=admin@genesis.local
GENESIS_ADMIN_PASSWORD=$ADMIN_PASS
ENV

echo "Admin: admin@genesis.local"
echo "Password: $ADMIN_PASS"
fi

./scripts/healthcheck.sh || true

echo "Genesis Termux installation complete."
