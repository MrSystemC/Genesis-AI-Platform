# QA report — Genesis AI Platform v1.0

The release was validated in the build environment before packaging.

## Automated API / product flow

`python -m pytest -q`

Result at final build stage: **2 passed**.

The end-to-end suite covers substantially more than two isolated assertions. It verifies:

- health endpoint;
- account registration and sign-in;
- default Free plan and workspace bootstrap;
- world creation with representative agents;
- world start and manual 12-step simulation;
- persistent snapshots and event generation;
- scenario analytics;
- custom agent deployment with goal/skills;
- agent task execution and memory growth;
- API-key creation and API-key authentication;
- full world export;
- workspace member addition;
- researcher access to shared world;
- viewer read access plus mutation denial;
- manual billing mode detection;
- password change and immediate invalidation of the old session token;
- administrator sign-in and global statistics;
- administrator plan change;
- Free-plan world limit enforcement.

## Autonomous supervisor

A separate runtime test launched the application with `GENESIS_AUTORUN=1` and a short tick interval, started a world, waited, and confirmed that the stored world age advanced automatically.

Result: **passed**.

## Live HTTP smoke test

Uvicorn was launched on a local port and the following flow was executed over real HTTP rather than the in-process test client:

1. `GET /api/v1/health`;
2. account registration;
3. world creation;
4. world start;
5. manual simulation ticks;
6. world-state/analytics response validation.

Result: **passed**.

## Frontend validation

- `node --check web/assets/app.js` — **passed**.
- The console was rendered in a headless Chromium session against a deterministic mock API.
- Dashboard and Simulation Lab produced **zero JavaScript page errors**.
- The Simulation Lab rendered agent nodes/links, HUD, world vitals, event history and timeline curves.

Reference screenshots are included in `docs/screenshots/`.

## Static / launch checks

- `python -m compileall -q genesis` — passed.
- Python AST parse of all production modules — passed.
- `bash -n` for Linux/Termux shell launchers — passed.
- Seed-demo script executed against a clean database and generated a paused world with 64 agents plus historical snapshots/events — passed.

Docker Compose was prepared but the build environment used for this audit did not provide the Docker CLI, so `docker compose config/build` itself was not executed here. The container configuration uses the same tested pinned Python requirements and production entrypoint as the local runtime.
