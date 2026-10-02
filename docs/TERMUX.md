# Termux launch

Genesis v1 deliberately uses a self-contained frontend and SQLite by default so it can run on Android without Node.js, Docker or a separate database service.

## Install

```bash
pkg update -y
pkg install -y python unzip
unzip Genesis-AI-Platform-v1.0.zip
cd Genesis-AI-Platform-v1.0
./scripts/termux_install.sh
```

The installer creates `.venv`, installs Python dependencies, creates `.env`, generates a random signing secret and prints the generated administrator password.

## Start

```bash
./scripts/termux_start.sh
```

Open:

```text
http://127.0.0.1:8000
```

To access from another device on the same network, use the Android device's LAN IP and ensure local firewall/network policy permits the port. Do not expose the Termux development instance directly to the public internet.

## Stop

Press `Ctrl+C` in the Termux session running Uvicorn.

## Keep files accessible

The database is stored under the project directory in `data/genesis.db`. Back up the entire project directory or at minimum `.env` and `data/`.
