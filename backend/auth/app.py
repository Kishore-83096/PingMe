import hmac

from flask import Flask, request
from flask_cors import CORS

from config import NGINX_PROXY_TOKEN
from routes import auth_bp


def create_app():
    app = Flask(__name__)

    # --------------------------------------------------
    # CORS
    # --------------------------------------------------
    # Allow the local React frontend to call the API.
    # The proxy token is NOT allowed here because the
    # browser must never know or send that secret.
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": [
                    "http://localhost:5173",
                ],
                "methods": [
                    "GET",
                    "POST",
                    "PUT",
                    "PATCH",
                    "DELETE",
                    "OPTIONS",
                ],
                "allow_headers": [
                    "Content-Type",
                    "Authorization",
                    "Accept",
                ],
            }
        },
    )

    # --------------------------------------------------
    # Nginx proxy authentication
    # --------------------------------------------------
    @app.before_request
    def validate_nginx_proxy():
        token = request.headers.get("X-PingMe-Proxy-Token")

        if not token or not hmac.compare_digest(
            token,
            NGINX_PROXY_TOKEN,
        ):
            return {
                "status": "error",
                "message": "Invalid proxy authentication",
            }, 403

    # --------------------------------------------------
    # Routes
    # --------------------------------------------------
    app.register_blueprint(
        auth_bp,
        url_prefix="/api/auth",
    )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
    )