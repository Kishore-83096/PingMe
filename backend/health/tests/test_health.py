from unittest.mock import patch

from app import create_app


def test_health():
    app = create_app()
    client = app.test_client()

    with patch("routes.check_redis_connection", return_value=True):
        response = client.get(
            "/api/health/",
            headers={
                "X-PingMe-Proxy-Token": "ci-test-token",
            },
        )

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {
        "database": "connected",
        "redis": "connected",
        "status": "ok",
    }


def test_legacy_health_route_uses_health_check():
    app = create_app()
    client = app.test_client()

    with (
        patch("routes.check_database_connection", return_value=True),
        patch("routes.check_redis_connection", return_value=True),
    ):
        response = client.get(
            "/api/auth/health",
            headers={
                "X-PingMe-Proxy-Token": "ci-test-token",
            },
        )

    assert response.status_code == 200
    assert response.get_json() == {
        "database": "connected",
        "redis": "connected",
        "status": "ok",
    }