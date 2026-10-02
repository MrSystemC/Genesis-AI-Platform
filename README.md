# Genesis AI Platform v1.0

**Infrastructure for autonomous AI worlds, agent societies and scenario simulation.**

Genesis turns the original autonomous-civilization project into a clean, launchable SaaS foundation. The production runtime is intentionally separated from the historical experimental branches while preserving the central idea: autonomous agents live inside persistent worlds, accumulate knowledge, affect economies and institutions, and create an inspectable history over time.

## What is included

- **Genesis Console** — self-contained responsive web UI, no CDN required.
- **World Engine** — persistent world state, time, population, economy, technology, stability, resources and knowledge.
- **Agent Runtime** — representative autonomous agents with roles, energy, knowledge, influence, wealth, mood and memory.
- **Simulation Lab** — start/pause/manual-step controls, speed control, animated world view and event stream.
- **Scenario templates** — Genesis Earth, Market Lab, AI Workforce Lab and Civilization Stress Test.
- **Analytics** — state timeline plus scenario-derived signals, risks and opportunities.
- **Accounts & workspaces** — registration, signed sessions, workspace membership and role-based access.
- **API keys** — hashed at rest; raw secret shown once.
- **Plan enforcement** — Free, Creator, Professional and Enterprise entitlements.
- **Admin console** — platform metrics, account inspection, plan changes and audit history.
- **Audit log** — security- and operations-relevant actions.
- **REST/OpenAPI** — documented FastAPI API at `/docs`.
- **Docker / Linux / Termux** launch paths.
- **Legacy reference** — selected original Genesis sources and the 20.x–30.x installer lineage, kept outside the production import path.

## Fastest local launch

```bash
unzip Genesis-AI-Platform-v1.0.zip
cd Genesis-AI-Platform-v1.0
./install.sh
./start.sh
```

Open: `http://127.0.0.1:8000`

`install.sh` creates a local virtual environment, installs dependencies, generates a random signing secret and generates a first administrator password in `.env`. The generated admin credentials are printed once during installation.

## Docker

```bash
cp .env.example .env
# Change GENESIS_SECRET_KEY and GENESIS_ADMIN_PASSWORD before public use.
docker compose up -d --build
```

Open: `http://localhost:8000`

## Termux (Android)

```bash
pkg install unzip -y
unzip Genesis-AI-Platform-v1.0.zip
cd Genesis-AI-Platform-v1.0
./scripts/termux_install.sh
./scripts/termux_start.sh
```

Then open `http://127.0.0.1:8000` in the device browser.

## Product model

Genesis is organized around the flow:

```text
User / API client
      │
      ▼
Workspace & access control
      │
      ▼
World instance
      │
      ├── Agent runtime
      ├── Civilization dynamics
      ├── Economy / resources
      ├── Events / history
      └── Analytics
      │
      ▼
Console / REST API / export
```

A world is a scenario environment, not a prediction oracle. Genesis produces **scenario-derived** outputs. Real-world business or policy decisions should use validated external data and domain models rather than treating simulated outcomes as forecasts.

## Runtime stack

- Python 3.11+
- FastAPI
- SQLAlchemy 2.x
- SQLite by default for local/Termux
- PostgreSQL supported through `DATABASE_URL` with `requirements-postgres.txt`
- Vanilla HTML/CSS/JS frontend served by the same process

The default single-process supervisor is appropriate for a first commercial deployment and demonstrations. For very large workloads, simulation workers can later be separated behind a queue without changing the public API model.

## Main directories

```text
genesis/             production backend/runtime
web/                 Genesis Console UI
scripts/             Linux and Termux installers/launchers
tests/               end-to-end test suite
deploy/              Nginx and systemd examples
docs/                architecture, API, security and deployment docs
legacy_reference/    selected historical Genesis code; never imported in production
data/                runtime database volume
```

## Security defaults

- Passwords: PBKDF2-HMAC-SHA256 with per-user random salts.
- Session tokens: HMAC-SHA256 signed, expiring tokens.
- API keys: only SHA-256 hashes are stored.
- Authorization: user/admin account roles plus workspace roles.
- Audit log: sign-in, world lifecycle, API-key and admin actions.
- Container: non-root runtime user.
- No secret is intentionally committed in the release; use `.env`.

Read `docs/SECURITY.md` before exposing Genesis publicly.

## Tests

```bash
python -m pytest -q
```

The included end-to-end suite verifies registration, authentication, world creation, simulation progression, analytics, API keys, export, workspace collaboration, Free-plan limits and admin access.

## Documentation

- `docs/PRODUCT.md` — positioning, users, value and monetization.
- `docs/ARCHITECTURE.md` — system components and boundaries.
- `docs/API.md` — core API surface.
- `docs/DEPLOYMENT.md` — local, Docker and server deployment.
- `docs/TERMUX.md` — Android/Termux instructions.
- `docs/SECURITY.md` — security model and production checklist.
- `docs/LEGACY_MIGRATION.md` — how the supplied Genesis-0 code was consolidated.
- `docs/RELEASE_CHECKLIST.md` — launch checklist and external credentials that must be supplied by the operator.

## Version

`1.0.0` — clean SaaS foundation release.

## Seed an investor/demo environment

After installation:

```bash
./scripts/seed_demo.sh
```

This creates a Creator demo account and a paused `Genesis Earth Demo` world with 64 representative agents and 40 years of event/snapshot history. If the demo account is new, the generated password is printed once.

## QA evidence

See `docs/QA_REPORT.md` and `docs/screenshots/` for the release verification summary and console render checks.
