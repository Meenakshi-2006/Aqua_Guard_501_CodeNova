<<<<<<< HEAD
=======
<<<<<<< HEAD

from datetime import datetime, timezone

from sqlalchemy import (
    String, Integer, Float, DateTime,
    ForeignKey, Text
)
from sqlalchemy.orm import Mapped, mapped_column

from database.db import Base


def utc_now():
    return datetime.now(timezone.utc)


class Alert(Base):

    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id"),
        nullable=False,
        index=True
    )

    sensor_id: Mapped[int | None] = mapped_column(
        ForeignKey("sensors.id"),
        nullable=True
    )

    detection_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )

    severity: Mapped[str] = mapped_column(
        String(20), nullable=False
    )

    reason: Mapped[str] = mapped_column(
        Text, nullable=False
    )

    estimated_liters: Mapped[float] = mapped_column(
        Float, default=0.0
    )

    estimated_cost: Mapped[float] = mapped_column(
        Float, default=0.0
    )

    status: Mapped[str] = mapped_column(
        String(30), default="open"
    )

    detected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )
=======
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from database.db import Base


class Alert(Base):
    __tablename__ = "alerts"

    # Unique ID for every alert
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Sensor and location associated with the alert
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)

    # Alert information
    alert_type = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)

    # Alert status: active, acknowledged, resolved
    status = Column(String(20), default="active", nullable=False)

    # Time the alert was created
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Time the alert was resolved (if resolved)
    resolved_at = Column(DateTime, nullable=True)

    def to_dict(self):
        """Convert the alert into a dictionary for API responses."""
        return {
            "id": self.id,
            "sensor_id": self.sensor_id,
            "location_id": self.location_id,
            "alert_type": self.alert_type,
            "severity": self.severity,
            "message": self.message,
            "status": self.status,
            "created_at": (
                self.created_at.isoformat() if self.created_at else None
            ),
            "resolved_at": (
                self.resolved_at.isoformat() if self.resolved_at else None
            ),
        }
>>>>>>> 00611ea25a561e5195be5805c83264be922e4988
>>>>>>> 91e46f88b20ea47e324ad904b27769a21f9a9ab8
