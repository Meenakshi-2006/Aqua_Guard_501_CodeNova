import pandas as pd


def analyze_night_flow(df, threshold_multiplier=1.5):
    """
    Analyze water consumption between 2 AM and 4 AM.

    Flags locations whose night flow is significantly above
    their historical night-flow average.
    """

    df = df.copy()

    df["recorded_at"] = pd.to_datetime(
        df["recorded_at"], errors="coerce"
    )
    df["consumption"] = pd.to_numeric(
        df["consumption"], errors="coerce"
    )

    df = df.dropna(subset=["recorded_at", "consumption"])

    df["hour"] = df["recorded_at"].dt.hour

    night_data = df[(df["hour"] >= 2) & (df["hour"] < 4)]

    if night_data.empty:
        return []

    results = []

    for location_id, group in night_data.groupby("location_id"):
        baseline = group["consumption"].mean()
        latest = group["consumption"].iloc[-1]

        if baseline > 0 and latest > baseline * threshold_multiplier:
            results.append({
                "location_id": location_id,
                "night_baseline": round(float(baseline), 2),
                "latest_night_consumption": round(float(latest), 2),
                "possible_night_leak": True
            })

    return results