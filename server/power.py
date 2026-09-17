import threading
import time

import pynvml


class GpuPowerMonitor:
    def __init__(self, sample_interval: float = 0.2):
        self.sample_interval = sample_interval
        self._power_samples = []
        self._utilization_samples = []
        self._stop_event = threading.Event()
        self._thread = None

    def _sample_loop(self):
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)

        try:
            while not self._stop_event.is_set():
                power_w = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0
                utilization_pct = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu

                self._power_samples.append(power_w)
                self._utilization_samples.append(utilization_pct)

                time.sleep(self.sample_interval)
        finally:
            pynvml.nvmlShutdown()

    def start(self):
        self._power_samples = []
        self._utilization_samples = []
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._sample_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()

        if not self._power_samples:
            return {
                "avg_power_w": 0.0,
                "avg_gpu_utilization_pct": 0.0,
                "sample_count": 0,
                "energy_wh": 0.0,
            }

        avg_power_w = sum(self._power_samples) / len(self._power_samples)
        avg_utilization_pct = sum(self._utilization_samples) / len(self._utilization_samples)
        duration_h = (len(self._power_samples) * self.sample_interval) / 3600

        return {
            "avg_power_w": round(avg_power_w, 2),
            "avg_gpu_utilization_pct": round(avg_utilization_pct, 1),
            "sample_count": len(self._power_samples),
            "energy_wh": round(avg_power_w * duration_h, 4),
        }


if __name__ == "__main__":
    monitor = GpuPowerMonitor()
    monitor.start()

    print("Olculuyor... (5 saniye)")
    time.sleep(5)

    result = monitor.stop()
    print(result)
