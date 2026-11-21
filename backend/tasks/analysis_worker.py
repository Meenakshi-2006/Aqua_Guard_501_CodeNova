
import pandas as pd

from backend.services.data_cleaning import clean_water_data
from backend.services.baseline_engine import (
    calculate_hourly_average,
    calculate_day_type_baseline,
    calculate_night_flow_baseline,
)
from backend.services.leak_detection import detect_leaks
from backend.services.night_flow_analysis import analyze_night_flow
from backend.services.gradual_leak_detection import detect_gradual_leaks
from backend.services.loss_estimation import estimate_water_loss
from backend.services.inspection_ranking import rank_inspections
from backend.services.notification_service import prepare_notifications


def run_analysis(df):
    """Run AquaGuard water-consumption analysis on input data."""

    cleaned_data = clean_water_data(df)

    if cleaned_data.empty:
        return {
            "success": False,
            "message": "No valid water consumption data available",
            "data": {}
        }

    # Calculate consumption baselines
    hourly_baseline = calculate_hourly_average(cleaned_data)
    day_type_baseline = calculate_day_type_baseline(cleaned_data)
    night_baseline = calculate_night_flow_baseline(cleaned_data)

    # Run leak analysis
    leak_alerts = detect_leaks(cleaned_data)
    night_alerts = analyze_night_flow(cleaned_data)
    gradual_alerts = detect_gradual_leaks(cleaned_data)

    # Combine alerts
    all_alerts = leak_alerts + night_alerts + gradual_alerts

    # Estimate excess water consumption
    total_consumption = float(cleaned_data["consumption"].sum())

    average_consumption = float(cleaned_data["consumption"].mean())

    water_loss = estimate_water_loss(
        total_consumption,
        average_consumption * len(cleaned_data)
    )

    # Rank locations for inspection
    ranked_inspections = rank_inspections(all_alerts)

    # Prepare notification data
    notifications = prepare_notifications(all_alerts)

    return {
        "success": True,
        "message": "AquaGuard analysis completed successfully",
        "data": {
            "total_records": len(cleaned_data),
            "total_consumption": round(total_consumption, 2),
            "hourly_baseline": hourly_baseline,
            "day_type_baseline": day_type_baseline,
            "night_flow_baseline": night_baseline,
            "possible_leaks": leak_alerts,
            "night_flow_alerts": night_alerts,
            "gradual_leak_alerts": gradual_alerts,
            "inspection_ranking": ranked_inspections,
            "notifications": notifications,
            "estimated_water_loss": water_loss
        }
    }
