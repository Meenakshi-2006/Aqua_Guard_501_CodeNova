

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-secret"
    )

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        ""
    ).strip()

    if not DATABASE_URL:
        DATABASE_URL = (
            "sqlite:///" +
            (BASE_DIR / "instance" / "aquaguard.db").as_posix()
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WATER_TARIFF = float(
        os.getenv("WATER_TARIFF", "25")
    )

    TIMEZONE = os.getenv(
        "TIMEZONE",
        "Asia/Kolkata"
    )
