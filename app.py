
from flask import Flask, request, jsonify, render_template
import sqlite3

from database import init_db
from traffic_manager import TrafficManager

app = Flask(__name__)
manager = TrafficManager()

init_db()


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# POST API - Insert traffic data
@app.route("/api/traffic", methods=["POST"])
def add_traffic():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON"}), 400

    road = data.get("road_name")
    count = data.get("vehicle_count")

    if not isinstance(road, str) or not road.strip():
        return jsonify({"error": "Invalid road name"}), 400

    if type(count) is not int or count < 0:
        return jsonify({"error": "Invalid vehicle count"}), 400

    with sqlite3.connect("traffic.db") as conn:
        conn.execute(
            """INSERT INTO traffic (road_name, vehicle_count)
               VALUES (?, ?)""",
            (road, count)
        )

    status = manager.check_congestion(count)

    return jsonify({
        "message": "Traffic data saved",
        "road": road,
        "vehicle_count": count,
        "status": status
    }), 201


# GET API - Retrieve traffic data
@app.route("/api/traffic", methods=["GET"])
def get_traffic():
    conn = sqlite3.connect("traffic.db")
    conn.row_factory = sqlite3.Row

    try:
        rows = conn.execute(
            """SELECT road_name, vehicle_count, timestamp
               FROM traffic
               ORDER BY timestamp DESC, id DESC
               LIMIT 20"""
        ).fetchall()
        return jsonify([dict(row) for row in rows])
    finally:
        conn.close()


# POST API - Recommend least congested road
@app.route("/api/recommend-route", methods=["POST"])
def recommend_route():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON"}), 400

    roads = data.get("roads")

    if not isinstance(roads, list) or not roads:
        return jsonify({"error": "Road list is required"}), 400

    for road in roads:
        if not isinstance(road, dict):
            return jsonify({"error": "Invalid road"}), 400

        name = road.get("name")
        count = road.get("vehicle_count")

        if not isinstance(name, str) or not name.strip():
            return jsonify({"error": "Invalid road name"}), 400

        if type(count) is not int or count < 0:
            return jsonify({"error": "Invalid vehicle count"}), 400

    best_road = manager.suggest_route(roads)

    return jsonify({
        "recommended_route": best_road["name"],
        "vehicle_count": best_road["vehicle_count"],
        "status": manager.check_congestion(
            best_road["vehicle_count"]
        )
    })


if __name__ == "__main__":
    app.run(debug=True)
