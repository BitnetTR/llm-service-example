import threading
import time

import pynvml


class GpuPowerMonitor:
    def __init__(self, sample_interval: float = 0.2):
        self.sample_interval = sample_interval
        self._samples = []
        self._stop_event = threading.Event()
        self._thread = None

    def _sample_loop(self):
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)

        try:
            while not self._stop_event.is_set():
                power_w = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0
                self._samples.append(power_w)
                time.sleep(self.sample_interval)
        finally:
            pynvml.nvmlShutdown()

    def start(self):
        self._samples = []
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._sample_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()

        if not self._samples:
            return {
                "avg_power_w": 0.0,
                "sample_count": 0,
                "energy_wh": 0.0,
            }

        avg_power_w = sum(self._samples) / len(self._samples)
        duration_h = (len(self._samples) * self.sample_interval) / 3600

        return {
            "avg_power_w": round(avg_power_w, 2),
            "sample_count": len(self._samples),
            "energy_wh": round(avg_power_w * duration_h, 4),
        }


if __name__ == "__main__":
    monitor = GpuPowerMonitor()
    monitor.start()

    print("Olculuyor... (5 saniye)")
    time.sleep(5)

    result = monitor.stop()
    print(result)
