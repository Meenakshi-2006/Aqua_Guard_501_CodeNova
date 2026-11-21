def estimate_water_loss(actual_consumption, baseline_consumption):
    """
    Estimate excess water consumption above the expected baseline.
    """

    actual = float(actual_consumption)
    baseline = float(baseline_consumption)

    if actual < 0 or baseline < 0:
        raise ValueError("Consumption values cannot be negative")

    estimated_loss = max(actual - baseline, 0)

    return {
        "actual_consumption": round(actual, 2),
        "baseline_consumption": round(baseline, 2),
        "estimated_excess": round(estimated_loss, 2),
        "possible_water_loss": round(estimated_loss, 2)
    }