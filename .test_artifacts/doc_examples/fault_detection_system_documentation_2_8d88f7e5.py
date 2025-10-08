# Example from: docs\fault_detection_system_documentation.md
# Index: 2
# Runnable: False
# Hash: 8d88f7e5

# example-metadata:
# runnable: false

# Initialize fault detector
fdi = FDIsystem(
    residual_threshold=0.1,
    persistence_counter=5,
    residual_states=[0, 1, 2],  # Position and first pendulum angle
    residual_weights=[2.0, 1.0, 3.0],  # Emphasize position and pendulum
    adaptive=True,
    cusum_enabled=True
)

# Fault detection loop
for t, measurement in simulation_data:
    status, residual = fdi.check(t, measurement, control_input, dt, dynamics)

    if status == "FAULT":
        logging.critical(f"Fault detected at t={t:.3f}s, residual={residual:.4f}")
        # Trigger safe shutdown or fault accommodation
        break