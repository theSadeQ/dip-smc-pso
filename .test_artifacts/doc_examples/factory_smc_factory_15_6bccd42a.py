# Example from: docs\reference\controllers\factory_smc_factory.md
# Index: 15
# Runnable: True
# Hash: 6bccd42a

from src.controllers.factory import create_all_smc_controllers

# Gains for each controller type
gains_dict = {
    "classical": [10, 8, 15, 12, 50, 0.01],
    "adaptive": [10, 8, 15, 12, 0.5],
    "sta": [25, 10, 15, 12, 20, 15],
    "hybrid": [15, 12, 18, 15]
}

# Create all controllers for comparison
controllers = create_all_smc_controllers(
    gains_dict,
    max_force=100.0,
    dt=0.01
)

# Simulate each controller
results = {}
for ctrl_name, controller in controllers.items():
    result = simulate(controller, duration=5.0)
    results[ctrl_name] = result
    print(f"{ctrl_name}: ITAE={result.itae:.3f}")