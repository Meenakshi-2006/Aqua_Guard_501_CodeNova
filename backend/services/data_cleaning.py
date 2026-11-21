import pandas as pd


def clean_water_data(df):
    """Clean water consumption data before analysis."""

    df = df.copy()

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove rows with missing important values
    required_columns = ["recorded_at", "consumption", "location_id"]
    df = df.dropna(subset=required_columns)

    # Convert date/time to proper format
    df["recorded_at"] = pd.to_datetime(
        df["recorded_at"], errors="coerce"
    )

    # Remove rows with invalid dates
    df = df.dropna(subset=["recorded_at"])

    # Convert consumption to numeric
    df["consumption"] = pd.to_numeric(
        df["consumption"], errors="coerce"
    )

    # Remove invalid consumption values
    df = df.dropna(subset=["consumption"])
    df = df[df["consumption"] >= 0]

    # Reset index
    df = df.reset_index(drop=True)

    return df