# Example from: docs\pso_optimization_workflow_user_guide.md
# Index: 9
# Runnable: False
# Hash: 45cbcd8f

# example-metadata:
# runnable: false

# HIL optimization with realistic constraints
hil_config = {
    'max_control_time': 0.001,  # 1ms control computation limit
    'actuator_bandwidth': 100,   # 100 Hz actuator bandwidth
    'sensor_noise_std': 0.01,    # 1% measurement noise
    'communication_delay': 0.0005  # 0.5ms delay
}

# Run optimization with HIL constraints
results = pso_tuner.optimize(
    bounds=bounds,
    hil_constraints=hil_config,
    real_time_validation=True
)