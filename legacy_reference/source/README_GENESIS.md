# GENESIS-0

## System
Genesis-0 Autonomous Civilization Platform

Version:
1.0.0

Stage:
production-ready

Status:
online


## Components

- Core Engine
- Autonomous Service
- Knowledge System
- Governance System
- Storage Layer
- Dashboard
- API


## Start

./start_genesis.sh


## API

Dashboard:
http://127.0.0.1:8000/genesis/dashboard

System:
http://127.0.0.1:8000/genesis/system

Health:
http://127.0.0.1:8000/genesis/health

Version:
http://127.0.0.1:8000/genesis/version


## Operator Commands

Start:

./genesis_operator.sh start


Stop:

./genesis_operator.sh stop


Restart:

./genesis_operator.sh restart


Status:

./genesis_operator.sh status


Health:

./genesis_operator.sh health


Backup:

./genesis_operator.sh backup


Version:

./genesis_operator.sh version


## Recovery

./recover_genesis.sh


## Package

GENESIS-0-FINAL-RELEASE.tar.gz


## Verification

Compile:

python -m py_compile api/server.py genesis_core.py autonomous_service.py


Snapshot:

python snapshot.py


## Architecture

Genesis Core controls simulation.

Autonomous Service executes cycles.

Knowledge stores information.

Governance manages decisions.

Storage preserves state.

Dashboard provides control interface.


## Production Status

Certified.
Locked.
Operational.

