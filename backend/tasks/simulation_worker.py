import threading
import time

from backend.services.sensor_manager import sensor_manager


_worker_thread = None
_stop_event = threading.Event()


def simulation_loop(interval_seconds=5):
    while not _stop_event.is_set():
        try:
            readings = sensor_manager.generate_all_readings()

            for reading in readings:
                print("Generated sensor reading:", reading)

        except Exception as error:
            print("Simulation worker error:", error)

        _stop_event.wait(interval_seconds)


def start_simulation(interval_seconds=5):
    global _worker_thread

    if _worker_thread is not None and _worker_thread.is_alive():
        return False

    if interval_seconds <= 0:
        raise ValueError("interval_seconds must be greater than zero")

    _stop_event.clear()

    _worker_thread = threading.Thread(
        target=simulation_loop,
        args=(interval_seconds,),
        daemon=True,
    )

    _worker_thread.start()
    return True


def stop_simulation():
    _stop_event.set()

    if _worker_thread is not None:
        _worker_thread.join(timeout=2)

    return True


if __name__ == "__main__":
    # Add a sample sensor so the worker has something to simulate.
    if sensor_manager.get_sensor("VS001") is None:
        sensor_manager.add_sensor("VS001", 1)

    print("Starting AquaGuard sensor simulation...")
    start_simulation(interval_seconds=5)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping simulation...")
        stop_simulation()