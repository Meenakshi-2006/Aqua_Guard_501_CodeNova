from flask import Blueprint, jsonify, request

from backend.services.sensor_manager import sensor_manager
from backend.services.sensor_health import check_sensor_health


sensor_bp = Blueprint("sensor", __name__)


@sensor_bp.route("/api/sensors", methods=["GET"])
def get_sensors():
    return jsonify({
        "success": True,
        "sensors": sensor_manager.get_all_sensors(),
    })


@sensor_bp.route("/api/sensors", methods=["POST"])
def add_sensor():
    data = request.get_json(silent=True) or {}

    sensor_id = data.get("sensor_id")
    location_id = data.get("location_id")

    if not sensor_id or location_id is None:
        return jsonify({
            "success": False,
            "error": "sensor_id and location_id are required",
        }), 400

    try:
        normal_flow = float(data.get("normal_flow", 30.0))

        if normal_flow < 0:
            raise ValueError

        sensor = sensor_manager.add_sensor(
            sensor_id=str(sensor_id),
            location_id=location_id,
            normal_flow=normal_flow,
        )

        return jsonify({
            "success": True,
            "message": "Sensor added successfully",
            "sensor_id": sensor.sensor_id,
        }), 201

    except ValueError as error:
        return jsonify({
            "success": False,
            "error": str(error) or "normal_flow must not be negative",
        }), 400


@sensor_bp.route("/api/sensors/<sensor_id>/readings", methods=["POST"])
def generate_reading(sensor_id):
    try:
        reading = sensor_manager.generate_reading(sensor_id)

        return jsonify({
            "success": True,
            "reading": reading,
        })

    except ValueError as error:
        return jsonify({
            "success": False,
            "error": str(error),
        }), 404


@sensor_bp.route("/api/sensors/<sensor_id>/readings", methods=["GET"])
def get_readings(sensor_id):
    try:
        readings = sensor_manager.get_readings(sensor_id)

        return jsonify({
            "success": True,
            "readings": readings,
        })

    except ValueError as error:
        return jsonify({
            "success": False,
            "error": str(error),
        }), 404


@sensor_bp.route("/api/sensors/<sensor_id>/scenario", methods=["POST"])
def change_scenario(sensor_id):
    data = request.get_json(silent=True) or {}
    scenario = data.get("scenario")

    if not scenario:
        return jsonify({
            "success": False,
            "error": "scenario is required",
        }), 400

    try:
        sensor_manager.set_sensor_scenario(sensor_id, scenario)

        return jsonify({
            "success": True,
            "message": "Sensor scenario updated",
            "scenario": scenario,
        })

    except ValueError as error:
        return jsonify({
            "success": False,
            "error": str(error),
        }), 400


@sensor_bp.route("/api/sensors/<sensor_id>/health", methods=["GET"])
def get_sensor_health(sensor_id):
    try:
        readings = sensor_manager.get_readings(sensor_id)

        if not readings:
            return jsonify({
                "success": True,
                "health": {
                    "status": "offline",
                    "message": "No readings received yet",
                },
            })

        health = check_sensor_health(readings[-1])

        return jsonify({
            "success": True,
            "health": health,
        })

    except ValueError as error:
        return jsonify({
            "success": False,
            "error": str(error),
        }), 404