
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
