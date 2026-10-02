# Security model

## Implemented in v1

- PBKDF2-HMAC-SHA256 password hashing with random 128-bit salts and 260,000 iterations.
- Expiring HMAC-SHA256 signed session tokens.
- API keys generated from cryptographically secure randomness and hashed at rest.
- Workspace-level roles: `admin`, `developer`, `researcher`, `viewer`.
- Platform-level `admin` role.
- Audit log for authentication, world lifecycle, workspace membership, API keys and admin changes.
- Non-root Docker user.
- Trusted-host middleware.
- Same-origin web console (no permissive CORS enabled by default).

## Before public internet launch

1. Set a unique `GENESIS_SECRET_KEY` generated from at least 32 random bytes.
2. Change/remove bootstrap admin credentials after first use.
3. Use HTTPS only.
4. Set `GENESIS_TRUSTED_HOSTS` to real hostnames instead of `*`.
5. Put the database password and payment-provider keys in a secret manager or protected `.env` with restrictive permissions.
6. Enable regular database backups and restoration tests.
7. Add upstream rate limiting (Nginx, CDN/WAF or API gateway) for `/auth/*`.
8. Add email verification/password reset through your chosen mail provider before broad consumer signup.
9. Run dependency vulnerability scanning as part of CI.
10. If multiple web workers are used, move the simulation supervisor to dedicated workers to avoid duplicate world ticks.

## Authentication scope

The token implementation is intentionally dependency-light for Linux/Termux portability. For a larger enterprise deployment, it can be replaced by an OIDC provider without changing world/workspace authorization rules.

## Data claims

Genesis simulation output is scenario-derived. The application must not market generated results as validated real-world predictions unless the deployed model has been calibrated and independently validated for that specific use case.
