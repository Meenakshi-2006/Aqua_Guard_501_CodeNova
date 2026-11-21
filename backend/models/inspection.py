
from datetime import datetime

from sqlalchemy import (
    String, Integer, DateTime, ForeignKey, Text
)
from sqlalchemy.orm import Mapped, mapped_column

from database.db import Base


class Inspection(Base):

    __tablename__ = "inspections"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    alert_id: Mapped[int] = mapped_column(
        ForeignKey("alerts.id"),
        nullable=False,
        index=True
    )

    inspector_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    findings: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(30), default="pending"
    )

    inspected_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
