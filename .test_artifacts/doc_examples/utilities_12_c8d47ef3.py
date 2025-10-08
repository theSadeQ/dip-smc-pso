# Example from: docs\guides\api\utilities.md
# Index: 12
# Runnable: True
# Hash: c8d47ef3

from src.utils.monitoring import MemoryMonitor

mem_monitor = MemoryMonitor(threshold_mb=500)

# Check memory periodically
while running:
    if alert := mem_monitor.check():
        print(alert)  # "Alert: 550MB > 500MB"
        # Clean up
        history = controller.initialize_history()
        import gc
        gc.collect()