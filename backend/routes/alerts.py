from flask import Blueprint, jsonify

alerts_bp = Blueprint("alerts", __name__, url_prefix="/api/alerts")


@alerts_bp.route("/", methods=["GET"])
def get_alerts():
    return jsonify({
        "success": True,
        "message": "Alerts fetched successfully",
        "alerts": []
    }), 200


@alerts_bp.route("/<int:alert_id>", methods=["GET"])
def get_alert(alert_id):
    return jsonify({
        "success": True,
        "alert_id": alert_id,
        "message": "Alert details fetched"
    }), 200


@alerts_bp.route("/<int:alert_id>/status", methods=["PUT"])
def update_alert_status(alert_id):
    return jsonify({
        "success": True,
        "alert_id": alert_id,
        "message": "Alert status update endpoint ready"
    }), 200