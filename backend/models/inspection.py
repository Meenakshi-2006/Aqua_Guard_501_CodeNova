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