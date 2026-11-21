from backend.services.virtual_sensor import VirtualWaterSensor


class SensorManager:
    def __init__(self):
        self.sensors = {}
        self.readings = {}

    def add_sensor(self, sensor_id, location_id, normal_flow=30.0):
        if sensor_id in self.sensors:
            raise ValueError("Sensor ID already exists")

        sensor = VirtualWaterSensor(
            sensor_id=sensor_id,
            location_id=location_id,
            normal_flow=normal_flow,
        )

        self.sensors[sensor_id] = sensor
        self.readings[sensor_id] = []

        return sensor

    def get_sensor(self, sensor_id):
        return self.sensors.get(sensor_id)

    def get_all_sensors(self):
        return [
            {
                "sensor_id": sensor.sensor_id,
                "location_id": sensor.location_id,
                "scenario": sensor.current_scenario,
            }
            for sensor in self.sensors.values()
        ]

    def set_sensor_scenario(self, sensor_id, scenario):
        sensor = self.get_sensor(sensor_id)

        if sensor is None:
            raise ValueError("Sensor not found")

        sensor.set_scenario(scenario)
        return sensor

    def generate_reading(self, sensor_id):
        sensor = self.get_sensor(sensor_id)

        if sensor is None:
            raise ValueError("Sensor not found")

        reading = sensor.generate_reading()
        self.readings[sensor_id].append(reading)

        # Keep the latest 1,000 readings per sensor in memory.
        self.readings[sensor_id] = self.readings[sensor_id][-1000:]

        return reading

    def generate_all_readings(self):
        return [
            self.generate_reading(sensor_id)
            for sensor_id in list(self.sensors.keys())
        ]

    def get_readings(self, sensor_id):
        if sensor_id not in self.sensors:
            raise ValueError("Sensor not found")

        return self.readings[sensor_id]
sensor_manager = SensorManager()