# Example from: docs\reference\interfaces\hil_real_time_sync.md
# Index: 4
# Runnable: True
# Hash: 8bf785dd

from src.interfaces.hil.real_time_sync import AdaptiveSync

# Adaptive synchronizer
sync = AdaptiveSync(
    kp=0.1,  # Proportional gain
    target_rate=100.0  # 100 Hz
)

# Plant loop with adaptive timing
plant_time = 0.0
for step in range(10000):
    start = time.time()

    # Step dynamics
    plant.step(dt_adjusted)

    # Measure actual time
    actual_dt = time.time() - start

    # Adjust for next iteration
    dt_adjusted = sync.adjust_rate(actual_dt, step)

    plant_time += dt_adjusted