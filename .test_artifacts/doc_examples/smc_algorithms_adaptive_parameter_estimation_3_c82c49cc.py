# Example from: docs\reference\controllers\smc_algorithms_adaptive_parameter_estimation.md
# Index: 3
# Runnable: True
# Hash: c82c49cc

# Use in complete control loop
controller = create_controller(ctrl_type, config)
result = simulate(controller, duration=5.0)