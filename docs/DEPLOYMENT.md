# Deployment

## 1. Local Linux

```bash
./install.sh
./start.sh
```

The default database is `data/genesis.db`.

## 2. Docker

```bash
cp .env.example .env
# edit all secrets
docker compose up -d --build
```

The Compose file mounts a persistent `genesis_data` volume.

## 3. VPS / server

Recommended minimum for a small first deployment:

- 2 vCPU;
- 4 GB RAM;
- 20 GB SSD;
- Ubuntu/Debian class distribution;
- TLS termination at Nginx/Caddy/managed load balancer.

A sample `deploy/genesis.service` and `deploy/nginx.conf` are included.

Typical flow:

```bash
sudo useradd --system --home /opt/genesis genesis
sudo mkdir -p /opt/genesis
# copy release contents into /opt/genesis
cd /opt/genesis
sudo -u genesis ./install.sh
sudo cp deploy/genesis.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now genesis
```

Use your TLS tooling or reverse proxy to expose HTTPS. Do not expose a production login form over plain HTTP.

## 4. PostgreSQL

Install the optional driver:

```bash
. .venv/bin/activate
pip install -r requirements-postgres.txt
```

Then set, for example:

```text
DATABASE_URL=postgresql+psycopg://genesis:password@db-host/genesis
```

For production, create a restricted database user and use a secret manager rather than committing the password.

## 5. Backups

For SQLite, stop writes and back up `data/genesis.db` or use SQLite's online backup tooling.

For PostgreSQL, use managed snapshots plus regular `pg_dump`/point-in-time recovery according to your hosting provider.

## 6. Updating

Before replacing the application code:

1. back up the database;
2. deploy the new release to a staging instance;
3. run the end-to-end tests;
4. confirm `/api/v1/health`;
5. switch traffic;
6. retain the previous release until the new one has been observed under real load.

### Docker + PostgreSQL profile

For a more production-oriented single-host deployment, install the PostgreSQL driver image and database service with the included override:

```bash
cp .env.example .env
# Set POSTGRES_PASSWORD plus all Genesis production secrets.
docker compose -f docker-compose.yml -f docker-compose.postgres.yml up -d --build
```

The application then uses PostgreSQL through `postgresql+psycopg://...` while the default Compose volume remains available for local SQLite deployments.
