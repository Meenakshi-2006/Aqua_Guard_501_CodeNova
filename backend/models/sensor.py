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