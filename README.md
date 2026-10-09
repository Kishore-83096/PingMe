# PingMe

PingMe is a secure messaging platform designed with a service-oriented backend architecture.

## Current Stage

The current implementation contains a Flask Health Service in `backend/health/` with:

- A health endpoint at `GET /api/health/`
- PostgreSQL and Redis/Valkey connectivity checks
- Nginx proxy-token validation
- Pytest health tests
- Docker support
- GitHub Actions CI

The Health Service is not an authentication service. The `backend/auth/` directory is reserved for a future Authentication Service; registration, login, and token lifecycle features are not implemented.

## Backend Environment

`backend/.env` is the environment file for the backend container. Start from `backend/.env.example` and supply local values there; do not commit `backend/.env`. Backend modules share this configuration.

## Health Check

```text
GET /api/health/
```

The endpoint returns HTTP 200 when PostgreSQL and Redis/Valkey are both connected, or HTTP 503 when either required dependency is unavailable. Requests continue to require the internal proxy token supplied by Nginx. The legacy `GET /api/auth/health` route remains temporarily available for compatibility.
