# Example from: docs\guides\api\utilities.md
# Index: 13
# Runnable: True
# Hash: aa22a314

from src.utils.monitoring import LatencyMonitor

latency_monitor = LatencyMonitor(dt=0.01, deadline=0.01)

for timestep in range(n_steps):
    start = latency_monitor.start()

    # Compute control
    control = controller.compute_control(state, state_vars, history)

    # Check if deadline met
    missed = latency_monitor.end(start)
    if missed:
        print(f"Deadline miss at step {timestep}")

# Get statistics
stats = latency_monitor.get_stats()
print(f"Average latency: {stats['avg_latency']:.4f} s")
print(f"Deadline misses: {stats['miss_count']}/{n_steps}")