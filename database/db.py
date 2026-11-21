
from contextlib import contextmanager

from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import Config


DATABASE_URL = Config.SQLALCHEMY_DATABASE_URI


# Database engine options
engine_options = {
    "pool_pre_ping": True
}

if DATABASE_URL.startswith("sqlite"):
    engine_options["connect_args"] = {
        "check_same_thread": False
    }


# Create database engine
engine = create_engine(
    DATABASE_URL,
    **engine_options
)


# Enable SQLite foreign keys
if DATABASE_URL.startswith("sqlite"):

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


# Database session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)


# Base class for database models
class Base(DeclarativeBase):
    pass


def init_db():
    """
    Create all ORM-managed tables and
    initialize additional SQL-managed tables.
    """

    # Import models so SQLAlchemy registers them
    from backend.models.user import User
    from backend.models.location import Location
    from backend.models.sensor import Sensor
    from backend.models.reading import Reading
    from backend.models.alert import Alert
    from backend.models.inspection import Inspection

    # Create six model tables
    Base.metadata.create_all(bind=engine)

    # Create four additional tables
    from pathlib import Path

    schema_path = (
        Path(__file__).resolve().parent / "schema.sql"
    )

    schema = schema_path.read_text(encoding="utf-8")

    with engine.begin() as connection:
        for statement in schema.split(";"):
            statement = statement.strip()

            if statement:
                connection.exec_driver_sql(statement)

    print("AquaGuard database initialized successfully!")


@contextmanager
def get_db():
    """
    Safely manage a database session.
    Automatically commits on success and
    rolls back when an error occurs.
    """

    session = SessionLocal()

    try:
        yield session
        session.commit()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()


def check_connection():
    """Check database connectivity."""

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        print("Database connection successful!")
        return True

    except Exception as error:
        print("Database connection failed:", error)
        return False
