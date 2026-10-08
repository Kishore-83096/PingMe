from flask import Blueprint, jsonify

from database import check_database_connection


auth_bp = Blueprint("auth", __name__)


@auth_bp.get("/health")
def health_check():
    """
    Health endpoint for the PingMe authentication service.

    The API is considered healthy only when PostgreSQL
    is also reachable.
    """

    database_connected = check_database_connection()

    if database_connected:
        return jsonify(
            {
                "status": "ok",
                "database": "connected",
            }
        ), 200

    return jsonify(
        {
            "status": "error",
            "database": "disconnected",
        }
    ), 503