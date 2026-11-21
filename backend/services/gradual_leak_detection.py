import pandas as pd


def detect_gradual_leaks(df, window=7, increase_threshold=0.20):
    """
    Detect gradual increases in water consumption.

    window: number of consecutive periods used for comparison.
    increase_threshold: minimum relative increase (20% by default).
    """

    df = df.copy()

    df["recorded_at"] = pd.to_datetime(
        df["recorded_at"], errors="coerce"
    )
    df["consumption"] = pd.to_numeric(
        df["consumption"], errors="coerce"
    )

    df = df.dropna(subset=["recorded_at", "consumption"])
    df = df.sort_values("recorded_at")

    results = []

    for location_id, group in df.groupby("location_id"):
        group = group.set_index("recorded_at")

        # Calculate daily average consumption
        daily = group["consumption"].resample("D").mean().dropna()

        if len(daily) < window * 2:
            continue

        # Compare recent average against previous average
        recent = daily.tail(window).mean()
        previous = daily.iloc[-(window * 2):-window].mean()

        if previous > 0:
            increase = (recent - previous) / previous

            if increase >= increase_threshold:
                results.append({
                    "location_id": location_id,
                    "previous_average": round(float(previous), 2),
                    "recent_average": round(float(recent), 2),
                    "increase_percentage": round(float(increase * 100), 2),
                    "possible_gradual_leak": True
                })

    return results