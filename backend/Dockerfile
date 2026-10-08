FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY auth/requirements.txt ./auth/requirements.txt

RUN pip install --no-cache-dir -r ./auth/requirements.txt

COPY auth ./auth

WORKDIR /app/auth

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "run:app"]