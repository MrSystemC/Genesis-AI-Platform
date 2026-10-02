# API

Base path: `/api/v1`

Interactive documentation: `/docs`

## Authentication

Session token:

```http
Authorization: Bearer <signed-token>
```

External API key:

```http
X-API-Key: gsk_...
```

API-key secrets are displayed only once. The database stores only their SHA-256 digest.

## Core endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | service health |
| POST | `/auth/register` | create account |
| POST | `/auth/login` | sign in |
| GET/PATCH | `/me` | current profile |
| GET | `/workspaces` | accessible workspaces |
| GET | `/dashboard?workspace_id=...` | workspace summary |
| GET/POST | `/worlds` | list/create worlds |
| GET/PATCH/DELETE | `/worlds/{id}` | inspect/update/delete world |
| POST | `/worlds/{id}/start` | start autorun |
| POST | `/worlds/{id}/pause` | pause autorun |
| POST | `/worlds/{id}/tick` | advance N steps manually |
| GET | `/worlds/{id}/export` | export full world state/history |
| GET/POST/DELETE | `/workspace/members` | team access |
| GET/POST/DELETE | `/api-keys` | developer credentials |
| GET | `/marketplace` | scenario templates |
| GET | `/plans` | entitlement catalog |
| GET | `/admin/stats` | platform totals |
| GET/PATCH | `/admin/users` | admin user control |
| GET | `/admin/audit` | audit trail |

## Example

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"me@example.com","name":"Founder","password":"StrongPassword123"}'
```

Create a world with the returned Bearer token:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/worlds \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"name":"Genesis Earth","template":"genesis-earth","population":1000,"agent_count":36,"seed":42}'
```
