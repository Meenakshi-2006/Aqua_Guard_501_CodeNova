from backend.services.sensor_manager import SensorManager

manager = SensorManager()

manager.add_sensor("VS001", 1)
manager.add_sensor("VS002", 2)

print("All sensors:")
print(manager.get_all_sensors())
print("\nGenerated readings:")
print(manager.generate_all_readings())