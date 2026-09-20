from flask import Flask, request, jsonify
import os
import requests
import secrets

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")
FFC_API_KEY = os.environ.get("FFC_API_KEY")

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
    region = request.args.get("region", "IND").upper()

    # আমাদের API key check
    if key != API_KEY:
        return jsonify({
            "error": "Invalid API Key"
        }), 401

    if not uid:
        return jsonify({
            "error": "UID is required"
        }), 400

    if not uid.isdigit() or not 5 <= len(uid) <= 15:
        return jsonify({
            "error": "Invalid UID"
        }), 400

    if region not in ["IND", "SG", "BR"]:
        return jsonify({
            "error": "Invalid region. Use IND, SG or BR"
        }), 400

    if not FFC_API_KEY:
        return jsonify({
            "error": "Player data source API key is not configured"
        }), 500

    try:
        url = "https://developers.freefirecommunity.com/api/v1/info"

        response = requests.get(
            url,
            params={
                "uid": uid,
                "region": region
            },
            headers={
    "x-api-key": FFC_API_KEY,
    "User-Agent": "FreeFireInfoAPI/1.0"
            }
            },
            timeout=15
        )

        data = response.json()

        if response.status_code != 200:
            return jsonify({
                "error": "Player data API error",
                "details": data
            }), response.status_code

        basic = data.get("basicInfo", {})

        return jsonify({
            "uid": uid,
            "nickname": basic.get("nickname"),
            "level": basic.get("level"),
            "region": basic.get("region"),
            "accountId": basic.get("accountId"),
            "data": data
        })

    except Exception as e:
        return jsonify({
            "error": "Failed to fetch player data"
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
