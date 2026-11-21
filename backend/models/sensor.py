
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
