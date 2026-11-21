<<<<<<< HEAD

from datetime import datetime, timezone

from sqlalchemy import (
    String, Integer, DateTime, ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column

from database.db import Base


def utc_now():
    return datetime.now(timezone.utc)


class Sensor(Base):

    __tablename__ = "sensors"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    sensor_code: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )

    location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id"), nullable=False, index=True
    )

    sensor_type: Mapped[str] = mapped_column(
        String(50), default="virtual"
    )

    status: Mapped[str] = mapped_column(
        String(30), default="active"
    )

    installed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )
=======
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_name = Column(String(100), nullable=False)
    sensor_type = Column(String(50), nullable=True)
    location_id = Column(Integer, nullable=True)
    status = Column(String(20), default="active")

    def to_dict(self):
        return {
            "id": self.id,
            "sensor_name": self.sensor_name,
            "sensor_type": self.sensor_type,
            "location_id": self.location_id,
            "status": self.status,
        }
>>>>>>> 00611ea25a561e5195be5805c83264be922e4988
