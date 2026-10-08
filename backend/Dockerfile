FROM python:3.12-slim

WORKDIR /app

COPY auth/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY auth/ .

EXPOSE 5000

CMD ["python", "app.py"]