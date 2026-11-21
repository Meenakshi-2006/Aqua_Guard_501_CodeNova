import pandas as pd


def detect_leaks(df, baseline_threshold=1.5):
    """
    Detect unusually high water consumption.

    A reading is flagged when it is greater than 1.5 times
    its corresponding baseline.
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

    hourly_baseline = (
        df.groupby(["location_id", "hour"])["consumption"].mean()
    )

    results = []

    for _, row in df.iterrows():
        key = (row["location_id"], row["hour"])
        baseline = hourly_baseline.get(key, 0)

        if baseline > 0 and row["consumption"] > baseline * baseline_threshold:
            results.append({
                "location_id": row["location_id"],
                "recorded_at": str(row["recorded_at"]),
                "consumption": float(row["consumption"]),
                "baseline": float(baseline),
                "possible_leak": True
            })

    return results