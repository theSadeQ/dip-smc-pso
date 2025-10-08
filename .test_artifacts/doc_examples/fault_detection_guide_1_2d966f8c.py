# Example from: docs\fault_detection_guide.md
# Index: 1
# Runnable: True
# Hash: 2d966f8c

from src.fault_detection.fdi import FDIsystem
from src.core.dynamics import DoublePendulum
import numpy as np

# Create FDI system with calibrated threshold and hysteresis
fdi = FDIsystem(
    residual_threshold=0.150,     # Statistically calibrated (Issue #18)
    persistence_counter=10,
    residual_states=[0, 1, 2],    # Monitor position and angles
    hysteresis_enabled=True,      # Prevent oscillation near threshold
    hysteresis_upper=0.165,
    hysteresis_lower=0.135
)

# Create dynamics model for predictions
dynamics = DoublePendulum()

# Simulation loop with FDI monitoring
for t in np.arange(0, 10, 0.001):
    # Get measurement (in practice, from sensors)
    x_measured = get_sensor_data()

    # Get control input
    u = controller.compute_control(x_measured, x_ref, t)

    # FDI check
    status, residual_norm = fdi.check(
        t=t,
        meas=x_measured,
        u=u,
        dt=0.001,
        dynamics_model=dynamics
    )

    if status == "FAULT":
        print(f"FAULT DETECTED at t={t:.3f}s, residual={residual_norm:.3f}")
        # Implement safety response
        break

    # Continue simulation
    x_next = dynamics.step(x_measured, u, 0.001)