from flask import Blueprint, jsonify

from database import check_database_connection
from redis_client import check_redis_connection

health_bp = Blueprint("health", __name__)


@health_bp.get("/")
def health_check():
    """
    Health endpoint for the PingMe health service.

    The API is considered healthy only when PostgreSQL
    and Redis/Valkey are both reachable.
    """

    database_connected = check_database_connection()
    redis_connected = check_redis_connection()

    if database_connected and redis_connected:
        return jsonify(
            {
                "status": "ok",
                "database": "connected",
                "redis": "connected",
            }
        ), 200

    return jsonify(
        {
            "status": "error",
            "database": "connected" if database_connected else "disconnected",
            "redis": "connected" if redis_connected else "disconnected",
        }
    ), 503
