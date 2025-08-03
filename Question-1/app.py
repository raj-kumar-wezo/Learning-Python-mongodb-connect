from flask import Flask, jsonify
import json
from pathlib import Path

app = Flask(__name__)
DATA_FILE = Path(__file__).with_name("data.json")

@app.route("/api", methods=["GET"])
def get_data():
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data), 200
    except FileNotFoundError:
        return jsonify({"error": "data file not found"}), 500
    except json.JSONDecodeError:
        return jsonify({"error": "invalid json format"}), 500

if __name__ == "__main__":
    app.run(debug=True)
