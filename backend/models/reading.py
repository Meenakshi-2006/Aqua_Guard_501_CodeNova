<<<<<<< HEAD
=======
<<<<<<< HEAD

from datetime import datetime

from sqlalchemy import (
    String, Integer, Float, DateTime,
    ForeignKey, UniqueConstraint, CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column

from database.db import Base


class Reading(Base):

    __tablename__ = "readings"

    __table_args__ = (
        UniqueConstraint(
            "sensor_id",
            "timestamp",
            name="unique_sensor_reading"
        ),
        CheckConstraint(
            "flow_rate >= 0",
            name="non_negative_flow"
        )
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    sensor_id: Mapped[int] = mapped_column(
        ForeignKey("sensors.id"),
        nullable=False,
        index=True
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True
    )

    flow_rate: Mapped[float] = mapped_column(
        Float, nullable=False
    )

    source: Mapped[str] = mapped_column(
        String(30), default="virtual_sensor"
    )

    scenario: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )

    quality_status: Mapped[str] = mapped_column(
        String(30), default="valid"
    )
=======
from datetime import datetime

from sqlalchemy import Column, Integer, Float, DateTime, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Reading(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_id = Column(Integer, nullable=True)
    location_id = Column(Integer, nullable=True)
    consumption = Column(Float, nullable=False)
    unit = Column(String(20), default="litres")
    recorded_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "sensor_id": self.sensor_id,
            "location_id": self.location_id,
            "consumption": self.consumption,
            "unit": self.unit,
            "recorded_at": (
                self.recorded_at.isoformat()
                if self.recorded_at else None
            ),
        }
>>>>>>> 00611ea25a561e5195be5805c83264be922e4988
>>>>>>> 91e46f88b20ea47e324ad904b27769a21f9a9ab8
