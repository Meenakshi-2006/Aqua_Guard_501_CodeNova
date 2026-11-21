
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
