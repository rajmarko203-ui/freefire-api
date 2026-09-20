import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Render Environment Variables
FFC_API_KEY = os.getenv("FFC_API_KEY")
PLAYER_API_URL = os.getenv("PLAYER_API_URL")


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "message": "Free Fire Info API is running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok"
    })


@app.route("/freefireinfo/<uid>")
def player(uid):
    # Check API key configuration
    if not FFC_API_KEY:
        return jsonify({
            "error": "FFC_API_KEY is not configured on Render"
        }), 500

    # Check upstream API URL
    if not PLAYER_API_URL:
        return jsonify({
            "error": "PLAYER_API_URL is not configured on Render"
        }), 500

    region = "BD"

    try:
        response = requests.get(
            PLAYER_API_URL,
            params={
                "uid": uid,
                "region": region
            },
            headers={
                "x-api-key": FFC_API_KEY,
                "User-Agent": "FreeFireInfoAPI/1.0"
            },
            timeout=15
        )

        try:
            data = response.json()
        except ValueError:
            return jsonify({
                "error": "Upstream API returned invalid JSON",
                "status_code": response.status_code,
                "response": response.text[:500]
            }), 502

        if response.status_code != 200:
            return jsonify({
                "error": "Player data API error",
                "status_code": response.status_code,
                "details": data
            }), response.status_code

        basic = data.get("basicInfo", {})

        return jsonify({
            "uid": uid,
            "nickname": basic.get("nickname"),
            "level": basic.get("level"),
            "region": basic.get("region", region),
            "accountId": basic.get("accountId"),
            "data": data
        })

    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Upstream API request timed out"
        }), 504

    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Request to upstream API failed",
            "details": str(e)
        }), 502

    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(
        host="0.0.0.0",
        port=port
    )
