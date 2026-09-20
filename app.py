from flask import Flask, request, jsonify
import os
import secrets

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")

if not API_KEY:
    API_KEY = secrets.token_urlsafe(24)


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "message": "Free Fire Information API"
    })


@app.route("/player")
def player():
    key = request.args.get("key")
    uid = request.args.get("uid")
    region = request.args.get("region", "IND")

    if key != API_KEY:
        return jsonify({
            "error": "Invalid API Key"
        }), 401

    if not uid:
        return jsonify({
            "error": "UID is required"
        }), 400

    return jsonify({
        "uid": uid,
        "region": region,
        "status": "Data source not connected yet"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
