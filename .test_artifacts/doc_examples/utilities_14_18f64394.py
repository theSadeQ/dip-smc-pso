# Example from: docs\guides\api\utilities.md
# Index: 14
# Runnable: True
# Hash: 18f64394

from src.utils.monitoring import SaturationMonitor

sat_monitor = SaturationMonitor(max_force=100.0)

for control in control_sequence:
    sat_monitor.update(control)

# Get saturation statistics
stats = sat_monitor.get_statistics()
print(f"Saturation percentage: {stats['saturation_percentage']:.1f}%")
print(f"Total saturated steps: {stats['saturated_count']}")