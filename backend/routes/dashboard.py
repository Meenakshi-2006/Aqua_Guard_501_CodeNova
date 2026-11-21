
from flask import Blueprint, jsonify

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


@dashboard_bp.route("/", methods=["GET"])
def get_dashboard():
    return jsonify({
        "success": True,
        "message": "Dashboard data fetched successfully",
        "data": {
            "total_consumption": 0,
            "possible_leaks": 0,
            "active_sensors": 0,
            "estimated_water_loss": 0,
            "system_status": "online"
        }
    }), 200


@dashboard_bp.route("/overview", methods=["GET"])
def get_overview():
    return jsonify({
        "success": True,
        "message": "Water consumption overview fetched successfully",
        "data": []
    }), 200