<<<<<<< HEAD
=======
<<<<<<< HEAD

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
=======
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    location_id = Column(Integer, nullable=True)
    inspector_name = Column(String(100), nullable=False)
    findings = Column(Text, nullable=True)
    status = Column(String(30), default="pending")
    inspected_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "location_id": self.location_id,
            "inspector_name": self.inspector_name,
            "findings": self.findings,
            "status": self.status,
            "inspected_at": (
                self.inspected_at.isoformat()
                if self.inspected_at else None
            ),
        }
>>>>>>> 00611ea25a561e5195be5805c83264be922e4988
>>>>>>> 91e46f88b20ea47e324ad904b27769a21f9a9ab8
