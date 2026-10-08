from unittest.mock import patch

from app import create_app


def test_health():
    app = create_app()
    client = app.test_client()

    with patch("routes.check_redis_connection", return_value=True):
        response = client.get("/api/auth/health")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {
        "database": "connected",
        "redis": "connected",
        "status": "ok",
    }