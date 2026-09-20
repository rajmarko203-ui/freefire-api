from flask import Flask, request, jsonify
import secrets

app = Flask(__name__)

API_KEY = secrets.token_urlsafe(24)

@app.route("/")
def home():
    return "Free Fire Information API is running!"

@app.route("/generate-key")
def generate_key():
    return jsonify({
        "api_key": API_KEY
    })

@app.route("/player")
def player():
    key = request.args.get("key")
    uid = request.args.get("uid")
    region = request.args.get("region", "IND")

    if key != API_KEY:
        return jsonify({"error": "Invalid API Key"}), 401

    if not uid:
        return jsonify({"error": "UID is required"}), 400

    return jsonify({
        "uid": uid,
        "region": region,
        "message": "Player data source not connected yet"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
