from datetime import datetime, timezone


def check_sensor_health(reading, max_age_seconds=120):
    if not isinstance(reading, dict):
        return {
            "status": "invalid",
            "message": "Reading must be a dictionary",
        }

    required_fields = ["sensor_id", "timestamp", "flow_rate"]

    for field in required_fields:
        if field not in reading:
            return {
                "status": "invalid",
                "message": f"Missing field: {field}",
            }

    try:
        flow_rate = float(reading["flow_rate"])
        timestamp = datetime.fromisoformat(
            reading["timestamp"].replace("Z", "+00:00")
        )

        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)

    except (ValueError, TypeError):
        return {
            "status": "invalid",
            "message": "Invalid flow rate or timestamp",
        }

    if flow_rate < 0:
        return {
            "status": "invalid",
            "message": "Flow rate cannot be negative",
        }

    age_seconds = (
        datetime.now(timezone.utc) - timestamp.astimezone(timezone.utc)
    ).total_seconds()

    if age_seconds < -30:
        return {
            "status": "invalid",
            "message": "Reading timestamp is in the future",
        }

    if age_seconds > max_age_seconds:
        return {
            "status": "offline",
            "message": "No recent reading received",
        }

    return {
        "status": "online",
        "message": "Sensor is working normally",
    }


if __name__ == "__main__":
    from backend.services.virtual_sensor import VirtualWaterSensor

    sensor = VirtualWaterSensor("VS001", 1)
    reading = sensor.generate_reading()

    print(check_sensor_health(reading))