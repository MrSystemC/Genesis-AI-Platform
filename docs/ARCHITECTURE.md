# Architecture

## Design goals

The supplied Genesis-0 archive contained a strong conceptual core but multiple generations of API, database, dashboard and backup branches. v1 introduces one production path and moves legacy code outside the runtime import graph.

```text
Browser / SDK / API client
          │
          ▼
      FastAPI API
          │
   ┌──────┼────────┐
   │      │        │
 Auth  Workspace  Admin
   │      │        │
   └──────┼────────┘
          ▼
      World Service
          │
   ┌──────┼───────────┐
   │      │           │
 Agents  Engine     Analytics
   │      │           │
   └──────┼───────────┘
          ▼
     SQLAlchemy DB
```

## Components

### `genesis/app.py`
Application bootstrap, static console serving, DB initialization, administrator bootstrap and background supervisor lifecycle.

### `genesis/api.py`
Single versioned REST API (`/api/v1`). This replaces the old parallel `api/`, `api3/`, `api30/` and `api_layer/` runtime ambiguity.

### `genesis/database.py`
SQLAlchemy schema for users, workspaces, memberships, worlds, agents, events, snapshots, API keys and audit entries.

### `genesis/engine.py`
Deterministic-by-seed simulation dynamics. The model preserves the Genesis concepts of population, economy, resources, knowledge, technology, stability, events and autonomous agent adaptation.

### `genesis/background.py`
A single-process simulation supervisor. Running worlds advance automatically. Manual tick endpoints remain available for experiments and deterministic testing.

### `web/`
No-build web console. It intentionally avoids an npm build requirement, making the same release practical on Linux, Docker and Android/Termux.

## Persistence

Default:

```text
SQLite -> data/genesis.db
```

For a server deployment, set `DATABASE_URL` to a PostgreSQL SQLAlchemy URL and install `requirements-postgres.txt`.

## Simulation scale model

`population` is a world-level metric and can represent a large modeled population. `agents` are representative autonomous entities stored individually for live inspection and visualization. This avoids creating millions of database rows merely to display a large virtual population.

## Horizontal scaling path

The v1 supervisor is deliberately simple. To scale beyond one application process:

1. disable `GENESIS_AUTORUN` on web nodes;
2. move `tick_world()` execution into worker processes;
3. claim world jobs through a distributed queue/lease;
4. keep the REST schema unchanged;
5. place PostgreSQL behind the workers and web service.

This avoids prematurely forcing Redis/Celery/Kubernetes on local and Termux users while preserving an upgrade path.
