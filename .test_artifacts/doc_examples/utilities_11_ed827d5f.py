# Example from: docs\guides\api\utilities.md
# Index: 11
# Runnable: True
# Hash: ed827d5f

from src.utils.monitoring import PerformanceMonitor

monitor = PerformanceMonitor(dt=0.01)

# Start monitoring
monitor.start()

# During simulation
for t, state, control in simulation_loop:
    monitor.update(t, state, control)

    # Check metrics
    if monitor.get_current_ise() > 100:
        print("Warning: High ISE detected")

# Get final statistics
stats = monitor.get_statistics()
print(f"ISE: {stats['ise']:.4f}")
print(f"Max theta: {stats['max_theta']:.3f} rad")
print(f"Settling time: {stats['settling_time']:.2f} s")