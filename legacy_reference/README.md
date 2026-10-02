# Genesis legacy reference

This directory preserves selected source artifacts from the supplied `Genesis-0.zip` for lineage, comparison and future feature mining. It is **not imported by the production runtime**.

The original archive contained 1,342 extracted files, including 1,041 Python files, 40 versioned `install_genesis_*` scripts and multiple nested release packages. The largest historical backup tree (`backup_before_integration/`) contained 501 files. The clean v1 runtime deliberately does not depend on those backup branches.

Preserved here:

- original `README_GENESIS.md` and release metadata;
- original `main.py` civilization entrypoint;
- original `run_genesis.py` platform entrypoint;
- `genesis_core.py`, `genesis_runtime.py`, `autonomous_service.py`;
- selected agent memory/runtime, civilization AI, economy and platform modules;
- all top-level versioned installer scripts as a compact record of the 20.x → 30.x development lineage.

The active v1 implementation lives in `genesis/`, `web/` and `scripts/`.
