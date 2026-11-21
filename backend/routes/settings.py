from flask import Blueprint, jsonify, request

settings_bp = Blueprint("settings", __name__, url_prefix="/api/settings")


@settings_bp.route("/", methods=["GET"])
def get_settings():
    return jsonify({
        "success": True,
        "message": "Settings fetched successfully",
        "settings": {}
    }), 200


@settings_bp.route("/", methods=["PUT"])
def update_settings():
    data = request.get_json(silent=True) or {}

    return jsonify({
        "success": True,
        "message": "Settings update endpoint ready",
        "received_data": data
    }), 200