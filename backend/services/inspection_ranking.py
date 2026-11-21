def rank_inspections(leak_alerts):
    """
    Rank locations by leak severity for inspection.

    Higher severity and greater consumption increase
    the inspection priority.
    """

    priority_order = {
        "critical": 4,
        "high": 3,
        "medium": 2,
        "low": 1
    }

    ranked = []

    for alert in leak_alerts:
        severity = str(alert.get("severity", "low")).lower()

        score = priority_order.get(severity, 1)

        consumption = alert.get("consumption", 0) or 0

        score += float(consumption) / 100

        ranked.append({
            **alert,
            "inspection_score": round(score, 2)
        })

    ranked.sort(
        key=lambda item: item["inspection_score"],
        reverse=True
    )

    return ranked