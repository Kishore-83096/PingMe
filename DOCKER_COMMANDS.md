# PingMe — Docker & Development Commands

This file contains commonly used commands for building, running, testing, stopping, and removing the PingMe backend Docker container.

---

## 1. Build Docker Image

Run from the PingMe root directory:

```powershell
docker build -f backend/Dockerfile -t pingme-backend:stage1 ./backend
```

### Verify the image

```powershell
docker images pingme-backend
```

---

## 2. Run Docker Container

```powershell
docker run -d --name pingme-auth-stage1 -p 5000:5000 pingme-backend:stage1
```

---

## 3. Check Running Containers

```powershell
docker ps
```

---

## 4. Check All Containers

```powershell
docker ps -a
```

---

## 5. View Container Logs

```powershell
docker logs pingme-auth-stage1
```

### Follow logs continuously

```powershell
docker logs -f pingme-auth-stage1
```

Press `Ctrl + C` to stop following the logs.

---

## 6. Test Auth Health Endpoint

### PowerShell

```powershell
Invoke-RestMethod http://localhost:5000/health
```

Expected:

```text
status
------
ok
```

### Raw JSON

```powershell
curl.exe http://localhost:5000/health
```

Expected:

```json
{"status":"ok"}
```

### Browser

Open:

```text
http://localhost:5000/health
```

Expected:

```json
{"status":"ok"}
```

---

## 7. Run Tests Locally

From the PingMe root directory:

```powershell
cd backend/auth
pytest -v
```

Return to root:

```powershell
cd ../..
```

---

## 8. Run Tests Inside Docker

Make sure the container is running first.

```powershell
docker exec pingme-auth-stage1 python -m pytest -v
```

Expected:

```text
1 passed
```

---

## 9. Stop Docker Container

```powershell
docker stop pingme-auth-stage1
```

Verify:

```powershell
docker ps
```

---

## 10. Start an Existing Stopped Container

```powershell
docker start pingme-auth-stage1
```

---

## 11. Restart Container

```powershell
docker restart pingme-auth-stage1
```

---

## 12. Remove Docker Container

The container should normally be stopped first.

```powershell
docker rm pingme-auth-stage1
```

Verify:

```powershell
docker ps -a
```

---

## 13. Force Remove Container

```powershell
docker rm -f pingme-auth-stage1
```

---

## 14. Remove Docker Image

```powershell
docker rmi pingme-backend:stage1
```

Verify:

```powershell
docker images pingme-backend
```

---

## 15. Force Remove Docker Image

Only use this if Docker reports that the image is being used:

```powershell
docker rmi -f pingme-backend:stage1
```

---

## 16. Complete Docker Cleanup

```powershell
docker stop pingme-auth-stage1
docker rm pingme-auth-stage1
docker rmi pingme-backend:stage1
```

If the container is already stopped:

```powershell
docker rm pingme-auth-stage1
docker rmi pingme-backend:stage1
```

---

# 17. Complete Stage 1 Docker Test Flow

## Step 1 — Build

```powershell
docker build -f backend/Dockerfile -t pingme-backend:stage1 ./backend
```

## Step 2 — Run

```powershell
docker run -d --name pingme-auth-stage1 -p 5000:5000 pingme-backend:stage1
```

## Step 3 — Check Container

```powershell
docker ps
```

## Step 4 — Check Logs

```powershell
docker logs pingme-auth-stage1
```

## Step 5 — Check Health Endpoint

```powershell
curl.exe http://localhost:5000/health
```

Expected:

```json
{"status":"ok"}
```

## Step 6 — Run Tests Inside Container

```powershell
docker exec pingme-auth-stage1 python -m pytest -v
```

Expected:

```text
1 passed
```

## Step 7 — Stop

```powershell
docker stop pingme-auth-stage1
```

## Step 8 — Remove Container

```powershell
docker rm pingme-auth-stage1
```

## Step 9 — Remove Image

```powershell
docker rmi pingme-backend:stage1
```

---

# 18. Git Commands

## Check Repository Status

```powershell
git status
```

## Check Short Status

```powershell
git status --short
```

## Add All Changes

```powershell
git add .
```

## Commit Changes

```powershell
git commit -m "Update PingMe"
```

## Push Changes

```powershell
git push
```

---

# 19. GitHub Actions

GitHub Actions automatically runs when code is pushed.

```powershell
git add .
git commit -m "Update PingMe"
git push
```

Then open:

```text
GitHub Repository
    ↓
Actions
    ↓
PingMe CI
    ↓
Auth Health Tests
```

Expected:

```text
Checkout repository       ✓
Set up Python             ✓
Install dependencies      ✓
Run health tests          ✓
```

---

# 20. Useful Docker Information Commands

## List all Docker images

```powershell
docker images
```

## List running containers

```powershell
docker ps
```

## List all containers

```powershell
docker ps -a
```

## Inspect a container

```powershell
docker inspect pingme-auth-stage1
```

## Show Docker disk usage

```powershell
docker system df
```

---

# 21. Check Docker Version

```powershell
docker --version
```

More detailed information:

```powershell
docker version
```

---

# 22. Check Docker System

```powershell
docker info
```

---

# 23. Check Docker Images

```powershell
docker image ls
```

---

# 24. Check Container Processes

```powershell
docker top pingme-auth-stage1
```

---

# 25. Open a Shell Inside the Container

For debugging:

```powershell
docker exec -it pingme-auth-stage1 /bin/bash
```

If Bash is unavailable:

```powershell
docker exec -it pingme-auth-stage1 /bin/sh
```

Exit:

```bash
exit
```

---

# 26. PingMe Stage 1 Expected State

The current Stage 1 backend contains:

```text
PingMe/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── backend/
│   ├── auth/
│   │   ├── app/
│   │   ├── tests/
│   │   ├── requirements.txt
│   │   └── run.py
│   │
│   └── Dockerfile
│
├── .env
├── .env.example
├── .gitignore
├── .dockerignore
└── README.md
```

Auth service:

```text
GET /health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

# 27. Stage 1 Verification Checklist

```text
Docker image builds successfully       ✓
Docker container starts                ✓
Gunicorn starts                        ✓
Port 5000 is accessible                ✓
Health endpoint works                  ✓
Local pytest passes                    ✓
Docker pytest passes                   ✓
Container stops successfully           ✓
Container can be removed               ✓
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
http://localhost:5000/health
```

---

# 29. Quick Commands

### Build

```powershell
docker build -f backend/Dockerfile -t pingme-backend:stage1 ./backend
```

### Run

```powershell
docker run -d --name pingme-auth-stage1 -p 5000:5000 pingme-backend:stage1
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
curl.exe http://localhost:5000/health
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
