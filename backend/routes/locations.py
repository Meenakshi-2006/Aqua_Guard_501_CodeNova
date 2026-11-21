from flask import Blueprint, jsonify

location_bp = Blueprint("location", __name__, url_prefix="/api/locations")


# Get all locations
@location_bp.route("/", methods=["GET"])
def get_locations():
    return jsonify({
        "success": True,
        "message": "Hostel locations fetched successfully",
        "locations": []
    }), 200


# Get a specific location
@location_bp.route("/<int:location_id>", methods=["GET"])
def get_location(location_id):
    return jsonify({
        "success": True,
        "location_id": location_id,
        "message": "Location details fetched successfully"
    }), 200