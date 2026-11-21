
from datetime import datetime


def format_timestamp(timestamp):
    """Convert a timestamp into a readable format."""
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp)

    return timestamp.strftime("%d-%m-%Y %H:%M")


def calculate_percentage_change(previous, current):
    """Calculate percentage change between two values."""
    previous = float(previous)
    current = float(current)

    if previous == 0:
        return 0.0 if current == 0 else 100.0

    return round(((current - previous) / previous) * 100, 2)


def litres_to_kilolitres(litres):
    """Convert litres to kilolitres."""
    return round(float(litres) / 1000, 3)


def safe_round(value, digits=2):
    """Safely round a numeric value."""
    try:
        return round(float(value), digits)
    except (TypeError, ValueError):
        return 0.0
