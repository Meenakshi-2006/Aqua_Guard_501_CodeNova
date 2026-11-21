
from sqlalchemy import select, text

from database.db import init_db, get_db

from backend.models.location import Location
from backend.models.sensor import Sensor


LOCATIONS = [
    ("Hostel A", "Hostel"),
    ("Hostel B", "Hostel"),
    ("College Block A", "Academic Block"),
    ("College Block B", "Academic Block"),
    ("Canteen", "Food Facility")
]


def seed_database():

    # Create database tables
    init_db()

    with get_db() as db:

        # Insert locations
        for name, building in LOCATIONS:

            existing = db.scalar(
                select(Location).where(
                    Location.name == name
                )
            )

            if existing is None:

                location = Location(
                    name=name,
                    building=building,
                    description=f"Monitoring area: {name}"
                )

                db.add(location)

        # Ensure location IDs are generated
        db.flush()

        # Insert virtual sensors
        locations = db.scalars(
            select(Location)
        ).all()

        for location in locations:

            sensor_code = f"VS{location.id:03d}"

            existing = db.scalar(
                select(Sensor).where(
                    Sensor.sensor_code == sensor_code
                )
            )

            if existing is None:

                sensor = Sensor(
                    sensor_code=sensor_code,
                    location_id=location.id,
                    sensor_type="virtual",
                    status="active"
                )

                db.add(sensor)

        # Insert default water tariff
        db.execute(
            text("""
                INSERT OR IGNORE INTO system_settings
                (setting_key, setting_value)
                VALUES ('water_tariff', '25')
            """)
        )

    print("\nAquaGuard sample data inserted!")
    print("5 locations and 5 virtual sensors configured.")


if __name__ == "__main__":
    seed_database()
