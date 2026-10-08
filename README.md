# PingMe

PingMe is a secure messaging platform designed with a service-oriented backend architecture.

## Current Stage

The current implementation contains the initial Flask authentication service foundation with:

- Flask
- Health endpoint
- Pytest health test
- Docker support
- GitHub Actions CI

## Backend Environment

`backend/.env` is the environment file for the entire backend service and its Docker container. Start from `backend/.env.example` and provide the required local values there; do not commit `backend/.env`. All backend modules use the shared backend configuration.

## Authentication Health Check

```text
GET /api/auth/health