from flask import Blueprint, jsonify

analytics_bp = Blueprint("analytics", __name__, url_prefix="/api/analytics")


@analytics_bp.route("/", methods=["GET"])
def get_analytics():
    return jsonify({
        "success": True,
        "message": "Hostel analytics fetched successfully",
        "data": {
            "total_consumption": 0,
            "possible_leaks": 0,
            "active_sensors": 0,
            "estimated_water_loss": 0
        }
    }), 200


@analytics_bp.route("/hourly", methods=["GET"])
def get_hourly_analytics():
    return jsonify({
        "success": True,
        "message": "Hourly hostel consumption fetched successfully",
        "data": []
    }), 200


@analytics_bp.route("/baselines", methods=["GET"])
def get_baselines():
    return jsonify({
        "success": True,
        "message": "Hostel consumption baselines fetched successfully",
        "data": []
    }), 200


@analytics_bp.route("/anomalies", methods=["GET"])
def get_anomalies():
    return jsonify({
        "success": True,
        "message": "Abnormal water consumption fetched successfully",
        "data": []
    }), 200