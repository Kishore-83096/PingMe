from flask import Flask

from routes import auth_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
    )

