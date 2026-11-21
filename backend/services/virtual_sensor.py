import random
from datetime import datetime, timezone


class VirtualWaterSensor:
    def __init__(self, sensor_id, location_id, normal_flow=30.0):
        self.sensor_id = sensor_id
        self.location_id = location_id
        self.normal_flow = float(normal_flow)
        self.reading_count = 0
        self.current_scenario = "normal"

    def set_scenario(self, scenario):
        allowed = {
            "normal",
            "continuous_leak",
            "burst_leak",
            "gradual_leak",
        }

        if scenario not in allowed:
            raise ValueError(
                f"Invalid scenario. Choose one of: {', '.join(sorted(allowed))}"
            )

        self.current_scenario = scenario
        self.reading_count = 0

    def generate_reading(self):
        noise = random.uniform(-2, 2)

        if self.current_scenario == "normal":
            flow = self.normal_flow + noise

        elif self.current_scenario == "continuous_leak":
            flow = 85 + noise

        elif self.current_scenario == "burst_leak":
            flow = (
                self.normal_flow + noise
                if self.reading_count < 3
                else 140 + noise
            )

        elif self.current_scenario == "gradual_leak":
            flow = self.normal_flow + (self.reading_count * 3) + noise

        else:
            flow = self.normal_flow + noise

        self.reading_count += 1
        flow = max(0, round(flow, 2))

        return {
            "sensor_id": self.sensor_id,
            "location_id": self.location_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "flow_rate": flow,
            "unit": "L/hour",
            "source": "virtual_sensor",
            "scenario": self.current_scenario,
        }


if __name__ == "__main__":
    sensor=  VirtualWaterSensor("VS001", 1)

    for number in range(5):
        print(f"Reading {number + 1}: {sensor.generate_reading()}")