from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return {
        "message": "DevOps deployment works!",
        "environment": os.getenv("APP_ENV", "unknown")
    }

@app.route("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
