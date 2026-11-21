import pandas as pd


def calculate_hourly_average(df):
    """Calculate average water consumption for each hour."""
    df = df.copy()
    df["recorded_at"] = pd.to_datetime(df["recorded_at"])

    df["hour"] = df["recorded_at"].dt.hour

    hourly_average = df.groupby("hour")["consumption"].mean()

    return hourly_average.to_dict()


def calculate_day_type_baseline(df):
    """Calculate separate baselines for weekdays and weekends."""
    df = df.copy()
    df["recorded_at"] = pd.to_datetime(df["recorded_at"])

    df["day_type"] = df["recorded_at"].dt.dayofweek.apply(
        lambda day: "weekend" if day >= 5 else "weekday"
    )

    baseline = df.groupby(["day_type", "hour"])["consumption"].mean()

    return baseline.to_dict()


def calculate_night_flow_baseline(df):
    """Calculate average water consumption between 2 AM and 4 AM."""
    df = df.copy()
    df["recorded_at"] = pd.to_datetime(df["recorded_at"])

    df["hour"] = df["recorded_at"].dt.hour

    night_data = df[(df["hour"] >= 2) & (df["hour"] < 4)]

    night_baseline = night_data.groupby("location_id")["consumption"].mean()

    return night_baseline.to_dict()
