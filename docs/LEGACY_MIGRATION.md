# Consolidation of Genesis-0

## Supplied archive

The supplied `Genesis-0.zip` extracted to 1,342 files, including 1,041 Python source files. It included:

- 40 top-level versioned installers from `install_genesis_20_1.sh` through the 30.x line;
- multiple API generations (`api/`, `api3/`, `api30/`, `api_layer/`);
- multiple database generations (`database/`, `database3/`, `database30/`);
- multiple dashboard/runtime generations;
- a 501-file `backup_before_integration/` tree;
- seven nested `.tar.gz` release bundles;
- the original civilization entrypoint and a later platform-oriented entrypoint.

The original README described the project as `Genesis-0 Autonomous Civilization Platform`, version `1.0.0`, with Core Engine, Autonomous Service, Knowledge System, Governance System, Storage Layer, Dashboard and API.

## What was preserved conceptually

The clean runtime retains the main Genesis ideas:

- persistent worlds;
- autonomous agents;
- knowledge accumulation;
- economy and resource dynamics;
- governance/social stability as system-level state;
- history/events;
- long-running autonomous simulation;
- API and visual control center.

## What changed

### One production API
The old server imported dozens of experimental modules and started an autonomous background thread during module import. v1 uses one `/api/v1` implementation and manages the supervisor through FastAPI application lifecycle hooks.

### One data model
The prior project had several independent storage/database generations. v1 uses one SQLAlchemy model and one configured `DATABASE_URL`.

### Explicit SaaS ownership
Users, workspaces, memberships, plan limits, API keys and audit logs are first-class entities instead of being scattered across experimental modules.

### Legacy isolated from runtime
Selected original files are retained under `legacy_reference/` for provenance and feature mining. Production code does not import them.

## Why not copy every old module into production

The archive contains overlapping and sometimes incompatible generations. Keeping all of them on the live import path would preserve historical code at the cost of reliability. v1 preserves the product idea and selected source lineage while giving the release a deterministic boot path and testable behavior.
