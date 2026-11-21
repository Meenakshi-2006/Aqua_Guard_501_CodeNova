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