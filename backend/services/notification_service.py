def create_notification(alert):
    """
    Create a notification message from an alert.
    """

    severity = str(alert.get("severity", "medium")).upper()
    location = alert.get("location_name", "Unknown location")
    message = alert.get("message", "Unusual water consumption detected")

    notification = {
        "title": f"{severity} Water Alert",
        "location": location,
        "message": message,
        "alert_id": alert.get("alert_id"),
        "timestamp": alert.get("timestamp"),
        "read": False
    }

    return notification


def prepare_notifications(alerts):
    """
    Convert a list of alerts into notification objects.
    """

    notifications = []

    for alert in alerts:
        notifications.append(create_notification(alert))

    return notifications