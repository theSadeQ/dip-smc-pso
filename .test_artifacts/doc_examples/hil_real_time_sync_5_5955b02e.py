# Example from: docs\reference\interfaces\hil_real_time_sync.md
# Index: 5
# Runnable: True
# Hash: 5955b02e

from src.interfaces.hil.real_time_sync import DeadlineMonitor

# Deadline monitor
monitor = DeadlineMonitor(
    deadline=0.01,  # 10 ms deadline
    tolerance=0.001  # 1 ms tolerance
)

# Control loop with deadline checking
for step in range(5000):
    start = time.time()

    # Compute control
    control = controller.compute(state)

    # Check deadline
    elapsed = time.time() - start
    if not monitor.check_deadline(elapsed):
        print(f"Deadline violation at step {step}: {elapsed*1000:.2f} ms")

# Report violations
print(f"Total violations: {monitor.violation_count}")
print(f"Violation rate: {monitor.violation_rate * 100:.2f}%")