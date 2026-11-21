
import pandas as pd


def validate_reading(data):
    """Validate a single water consumption reading."""

    required_fields = ["recorded_at", "consumption", "location_id"]

    for field in required_fields:
        if field not in data or data[field] is None:
            return {
                "valid": False,
                "message": f"Missing required field: {field}"
            }

    try:
        timestamp = pd.to_datetime(data["recorded_at"], errors="raise")
        consumption = float(data["consumption"])

        if consumption < 0:
            return {
                "valid": False,
                "message": "Consumption cannot be negative"
            }

        if pd.isna(timestamp) or pd.isna(consumption):
            return {
                "valid": False,
                "message": "Timestamp or consumption is invalid"
            }

    except (ValueError, TypeError):
        return {
            "valid": False,
            "message": "Invalid timestamp or consumption value"
        }

    return {
        "valid": True,
        "message": "Reading is valid"
    }


def validate_dataframe(df):
    """Validate required columns in a water consumption dataset."""

    required_columns = ["recorded_at", "consumption", "location_id"]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        return {
            "valid": False,
            "message": "Missing required columns",
            "missing_columns": missing_columns
        }

    return {
        "valid": True,
        "message": "Dataset structure is valid"
    }
