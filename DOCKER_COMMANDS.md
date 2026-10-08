# PingMe — Docker & Development Commands
This file contains commonly used commands for building, running, testing, stopping, and removing the PingMe authentication backend Docker container.

`backend/.env` is the shared environment file for the entire backend service/container. Use `backend/.env.example` as the safe template. The real environment file is supplied to Docker at runtime, not copied into the image.

---

## 1. Build Docker Image
Run from the PingMe root directory:

```
docker build --no-cache -f backend/Dockerfile -t pingme-backend:stage1 ./backend
```

### Verify the image

```
docker images pingme-backend
```

---

## 2. Run Docker Container
Run the container with the environment variables from `backend/.env`:

```
docker run -d --name pingme-auth-stage1 --env-file backend/.env -p 5000:5000 pingme-backend:stage1
```

> The `--env-file backend/.env` option injects the backend's runtime environment without adding the real environment file to the image.

---

## 3. Check Running Containers

```
docker ps
```
Expected:

```
pingme-auth-stage1
```

---

## 4. Check All Containers

```
docker ps -a
```

---

## 5. View Container Logs

```
docker logs pingme-auth-stage1
```

### Follow logs continuously

```
docker logs -f pingme-auth-stage1
```
Press `Ctrl + C` to stop following the logs.

---

# 6. Test Authentication Health Endpoint
The current PingMe authentication health endpoint is:

```
http://localhost:5000/api/auth/health
```
This endpoint checks the Flask service and verifies connectivity to Neon PostgreSQL.

### PowerShell

```
Invoke-RestMethod http://localhost:5000/api/auth/health
```
Expected:

```
database status
-------- ------
connected ok
```

### Raw JSON

```
curl.exe http://localhost:5000/api/auth/health
```
Expected:

```
{"database":"connected","status":"ok"}
```

### Browser
Open:

```
http://localhost:5000/api/auth/health
```
Expected:

```
{
  "database": "connected",
  "status": "ok"
}
```

### What the health endpoint verifies

```
Client
  ↓
Flask Authentication API
  ↓
/api/auth/health
  ↓
Database connection check
  ↓
Neon PostgreSQL
  ↓
SELECT 1
  ↓
Database connected
  ↓
HTTP 200
```
If PostgreSQL is unavailable, the endpoint returns:

```
{
  "database": "disconnected",
  "status": "error"
}
```
with HTTP status:

```
503 Service Unavailable
```

---

# 7. Run Tests Locally
The tests are located inside the authentication service.

From the PingMe root directory:

```
cd backend/auth
```
Run:

```
pytest -v
```
Return to the PingMe root directory:

```
cd ../..
```

> The health test calls the actual `/api/auth/health` endpoint and verifies the database-connected response.

---

# 8. Run Tests Inside Docker
Make sure the container is running first.

```
docker exec pingme-auth-stage1 python -m pytest -v
```
Expected:

```
============================= test session starts ==============================
...
tests/test_health.py::test_health PASSED
============================== 1 passed ==============================
```
The Docker test verifies the application from inside the same container environment.

---

### Run Ruff Inside Docker
Ruff is installed in the backend image, so linting can run in a temporary container without starting the API service:

```
docker run --rm pingme-backend:stage1 ruff check /app
```

Expected:

```
All checks passed!
```

Rebuild the image first if the source code or dependencies have changed. The `--rm` option removes the temporary container when Ruff finishes.

---

# 9. Stop Docker Container

```
docker stop pingme-auth-stage1
```
Verify:

```
docker ps
```

---

# 10. Start an Existing Stopped Container

```
docker start pingme-auth-stage1
```
Verify:

```
docker ps
```

---

# 11. Restart Container

```
docker restart pingme-auth-stage1
```

---

# 12. Remove Docker Container
The container should normally be stopped first.

```
docker rm pingme-auth-stage1
```
Verify:

```
docker ps -a
```

---

# 13. Force Remove Container
Use this if the container is still running:

```
docker rm -f pingme-auth-stage1
```

---

# 14. Remove Docker Image

```
docker rmi pingme-backend:stage1
```
Verify:

```
docker images pingme-backend
```

---

# 15. Force Remove Docker Image
Only use this if Docker reports that the image is being used:

```
docker rmi -f pingme-backend:stage1
```

---

# 16. Complete Docker Cleanup
If the container is running:

```
docker stop pingme-auth-stage1
docker rm pingme-auth-stage1
docker rmi pingme-backend:stage1
```
If the container is already stopped:

```
docker rm pingme-auth-stage1
docker rmi pingme-backend:stage1
```

---

# 17. Complete Stage 1 Docker Test Flow
This is the recommended complete verification sequence.

## Step 1 — Build Image

```
docker build --no-cache -f backend/Dockerfile -t pingme-backend:stage1 ./backend
```

## Step 2 — Run Ruff Lint Check

```
docker run --rm pingme-backend:stage1 ruff check /app
```

## Step 3 — Run Container

```
docker run -d --name pingme-auth-stage1 --env-file backend/.env -p 5000:5000 pingme-backend:stage1
```

## Step 4 — Check Container

```
docker ps
```
Expected:

```
pingme-auth-stage1
```

## Step 5 — Check Logs

```
docker logs pingme-auth-stage1
```
Expected Flask server:

```
* Serving Flask app 'app'
* Debug mode: off
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
```

## Step 6 — Check Health Endpoint

```
curl.exe http://localhost:5000/api/auth/health
```
Expected:

```
{"database":"connected","status":"ok"}
```

## Step 7 — Run Tests Inside Container

```
docker exec pingme-auth-stage1 python -m pytest -v
```
Expected:

```
1 passed
```

## Step 8 — Stop Container

```
docker stop pingme-auth-stage1
```

## Step 9 — Remove Container

```
docker rm pingme-auth-stage1
```

## Step 10 — Remove Image

```
docker rmi pingme-backend:stage1
```

---

# 18. Git Commands

## Check Repository Status

```
git status
```

## Check Short Status

```
git status --short
```

## Add All Changes

```
git add .
```

## Commit Changes

```
git commit -m "Update PingMe"
```

## Push Changes

```
git push
```

---

# 19. GitHub Actions
GitHub Actions automatically runs the CI workflow when code is pushed.

```
git add .
git commit -m "Update PingMe"
git push
```
Then open:

```
GitHub Repository
    ↓
Actions
    ↓
PingMe CI
    ↓
Auth Health Tests
```
Expected workflow stages:

```
Checkout repository       ✓
Gitleaks secret scan      ✓
Docker image build        ✓
Syntax, Ruff, and pytest  ✓
Backend and health checks ✓
```

> CI receives required values from GitHub Actions secrets and injects them into Docker at runtime; it does not use a developer's local `backend/.env`.

---

# 20. Useful Docker Information Commands

## List all Docker images

```
docker images
```

## List running containers

```
docker ps
```

## List all containers

```
docker ps -a
```

## Inspect a container

```
docker inspect pingme-auth-stage1
```

## Show Docker disk usage

```
docker system df
```

---

# 21. Check Docker Version

```
docker --version
```
More detailed information:

```
docker version
```

---

# 22. Check Docker System

```
docker info
```

---

# 23. Check Docker Images

```
docker image ls
```

---

# 24. Check Container Processes

```
docker top pingme-auth-stage1
```

---

# 25. Open a Shell Inside the Container
For debugging:

```
docker exec -it pingme-auth-stage1 /bin/bash
```
If Bash is unavailable:

```
docker exec -it pingme-auth-stage1 /bin/sh
```
Exit:

```
exit
```

---

# 26. Check Environment Variables Inside Container
Check that `DATABASE_URL` was injected without displaying its value:

```
docker exec pingme-auth-stage1 sh -c 'test -n "$DATABASE_URL" && echo DATABASE_URL is set'
```

This prints only whether the variable is set.

---

# 27. PingMe Stage 1 Directory Structure
Current Stage 1 structure:

```
PingME/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── backend/
│   ├── auth/
│   │   ├── app.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── routes.py
│   │   ├── requirements.txt
│   │   └── tests/
│   │       └── test_health.py
│   │
│   ├── .env
│   ├── .env.example
│   ├── .dockerignore
│   └── Dockerfile
│
├── .gitignore
├── .dockerignore
└── README.md
```

---

# 28. PingMe Authentication Service
Current authentication service health endpoint:

```
GET /api/auth/health
```
Expected successful response:

```
{
  "database": "connected",
  "status": "ok"
}
```
The endpoint verifies that:

1. Flask is running.
2. The authentication service is reachable.
3. `DATABASE_URL` is available.
4. The application can connect to Neon PostgreSQL.
5. PostgreSQL successfully responds to `SELECT 1`.

---

# 29. PingMe Stage 1 Verification Checklist

```
Docker image builds successfully       ✓

Docker container starts                ✓

Flask server starts                   ✓

Port 5000 is accessible               ✓

Authentication health endpoint works ✓

Neon PostgreSQL connection works      ✓

PostgreSQL health check works         ✓

Pytest passes                          ✓

Docker pytest passes                   ✓

Container stops successfully           ✓

Container can be removed                ✓

Image can be removed                    ✓
```

---

# 30. Important Current Values

### Docker Image

```
pingme-backend:stage1
```

### Docker Container

```
pingme-auth-stage1
```

### Authentication Port

```
5000
```

### Authentication Health Endpoint

```
http://localhost:5000/api/auth/health
```

### Database

```
Neon PostgreSQL
```

### Database Health Query

```
SELECT 1;
```

---

# 31. Quick Commands

### Build

```
docker build --no-cache -f backend/Dockerfile -t pingme-backend:stage1 ./backend
```

### Run

```
docker run -d --name pingme-auth-stage1 --env-file backend/.env -p 5000:5000 pingme-backend:stage1
```

### Check

```
docker ps
```

### Logs

```
docker logs pingme-auth-stage1
```

### Health

```
curl.exe http://localhost:5000/api/auth/health
```

### Tests

```
docker exec pingme-auth-stage1 python -m pytest -v
```

### Ruff lint

```
docker run --rm pingme-backend:stage1 ruff check /app
```

### Stop

```
docker stop pingme-auth-stage1
```

### Remove Container

```
docker rm pingme-auth-stage1
```

### Remove Image

```
docker rmi pingme-backend:stage1
```

### Git Push

```
git add .
git commit -m "Update PingMe"
git push
```

---

# 32. Current Stage 1 Architecture

```
                    PingMe Stage 1
                          │
                          ▼
                  ┌───────────────┐
                  │  Flask Auth   │
                  │     API       │
                  └───────┬───────┘
                          │
                          │ /api/auth/health
                          ▼
                  ┌───────────────┐
                  │    Health     │
                  │     Check     │
                  └───────┬───────┘
                          │
                          │ SELECT 1
                          ▼
                  ┌───────────────┐
                  │     Neon      │
                  │  PostgreSQL   │
                  └───────────────┘
```
Stage 1 currently focuses only on establishing and verifying the backend-to-database connection.

Authentication features such as registration, login, logout, JWT handling, password hashing, refresh tokens, sessions, and user tables will be implemented in later stages.

Image can be removed                   ✓
GitHub Actions CI passes               ✓
```

---

# 28. Important Current Values

### Docker Image

```text
pingme-backend:stage1
```

### Docker Container

```text
pingme-auth-stage1
```

### Auth Port

```text
5000
```

### Health Endpoint

```text
http://localhost:5000/api/auth/health
```

---

# 29. Quick Commands

### Build

```powershell
docker build --no-cache -f backend/Dockerfile -t pingme-backend:stage1 ./backend
```

### Run

```powershell
docker run -d --name pingme-auth-stage1 --env-file backend/.env -p 5000:5000 pingme-backend:stage1
```

### Check

```powershell
docker ps
```

### Logs

```powershell
docker logs pingme-auth-stage1
```

### Health

```powershell
curl.exe http://localhost:5000/api/auth/health
```

### Tests

```powershell
docker exec pingme-auth-stage1 python -m pytest -v
```

### Stop

```powershell
docker stop pingme-auth-stage1
```

### Remove Container

```powershell
docker rm pingme-auth-stage1
```

### Remove Image

```powershell
docker rmi pingme-backend:stage1
```

### Git Push

```powershell
git add .
git commit -m "Update PingMe"
git push
```

---

# 33. Nginx Stage 1 Docker Commands
Run these commands from the PingMe repository root. Nginx reads its runtime settings from `nginx/.env`; the environment file is passed to the container and is not copied into the image.

### Build the Nginx image

```powershell
docker build --no-cache -f nginx/Dockerfile -t pingme-nginx:stage1 ./nginx
```

### Run the Nginx container

```powershell
docker run -d `
  --name pingme-nginx-stage1 `
  --env-file nginx/.env `
  -p 8080:8080 `
  pingme-nginx:stage1
```

### Check the proxied health endpoint

```powershell
curl.exe http://localhost:8080/api/auth/health
```

Expected response:

```json
{"database":"connected","redis":"connected","status":"ok"}
```

### Stop the Nginx container

```powershell
docker stop pingme-nginx-stage1
```

### Remove the Nginx container

```powershell
docker rm pingme-nginx-stage1
```

### Remove the Nginx image

```powershell
docker rmi pingme-nginx:stage1
```
