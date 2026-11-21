from sqlalchemy import select, text  # type: ignore[reportMissingImports]

from database.db import check_connection, get_db

from backend.models.location import Location
from backend.models.sensor import Sensor


def test_database():

    print("\nDATABASE CONNECTION")

    if not check_connection():
        return

    with get_db() as db:

        locations = db.scalars(
            select(Location)
        ).all()

        sensors = db.scalars(
            select(Sensor)
        ).all()

        tables = db.execute(
            text("""
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                AND name NOT LIKE 'sqlite_%'
                ORDER BY name
            """)
        ).scalars().all()

        print("\nLOCATIONS")

        for location in locations:
            print(
                location.id,
                location.name,
                location.building
            )

        print("\nSENSORS")

        for sensor in sensors:
            print(
                sensor.sensor_code,
                sensor.location_id,
                sensor.status
            )

        print("\nTABLES")

        for table in tables:
            print(table)

        print("\nTotal locations:", len(locations))
        print("Total sensors:", len(sensors))
        print("Total application tables:", len(tables))


if __name__ == "__main__":
    test_database()
