import os

from flask import Flask, jsonify, render_template

app = Flask(__name__)


def app_details():
    return {
        "app_name": os.getenv("APP_NAME", "DevOps Delivery Lab"),
        "environment": os.getenv("APP_ENV", "local"),
        "version": os.getenv("APP_VERSION", "dev"),
    }


@app.get("/")
def home():
    return render_template("index.html", **app_details())


@app.get("/health")
def health():
    return jsonify(status="healthy")


@app.get("/api/status")
def api_status():
    details = app_details()
    return jsonify(
        service=details["app_name"],
        status="healthy",
        environment=details["environment"],
        version=details["version"],
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=False,
    )
