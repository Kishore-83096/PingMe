import hmac

from flask import Flask, request

from config import NGINX_PROXY_TOKEN
from routes import auth_bp


def create_app():
    app = Flask(__name__)

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