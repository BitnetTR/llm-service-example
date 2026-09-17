import pynvml

# NVML oturumunu başlat
pynvml.nvmlInit()

try:
    # Cihaz sayısını öğren ve her bir GPU'yu tara
    device_count = pynvml.nvmlDeviceGetCount()

    for i in range(device_count):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        name = pynvml.nvmlDeviceGetName(handle)

        # Güç tüketimi (miliwatt -> watt)
        power_mw = pynvml.nvmlDeviceGetPowerUsage(handle)
        power_w = power_mw / 1000.0

        # İsteğe bağlı: GPU kullanım yüzdesi ve Güç limiti
        utilization = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
        power_limit_w = pynvml.nvmlDeviceGetEnforcedPowerLimit(handle) / 1000.0

        print(f"GPU {i} ({name}):")
        print(f"  - Kullanım: %{utilization}")
        print(f"  - Anlık Güç: {power_w:.2f} W / Limit: {power_limit_w:.2f} W")

finally:
    # İşlem bitince NVML'i kapatmayı unutmayın
    pynvml.nvmlShutdown()