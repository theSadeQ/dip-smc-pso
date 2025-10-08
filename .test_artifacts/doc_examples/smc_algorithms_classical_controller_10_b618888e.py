# Example from: docs\reference\controllers\smc_algorithms_classical_controller.md
# Index: 10
# Runnable: True
# Hash: b618888e

from src.utils.monitoring.latency import LatencyMonitor

# Monitor control loop timing
monitor = LatencyMonitor(dt=0.01)

start = monitor.start()
control, state_vars, history = controller.compute_control(state, state_vars, history)
missed_deadlines = monitor.end(start)

if missed_deadlines > 0:
    print(f"Warning: {missed_deadlines} deadline misses detected!")