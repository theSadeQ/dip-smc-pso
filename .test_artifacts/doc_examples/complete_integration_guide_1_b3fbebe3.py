# Example from: docs\workflows\complete_integration_guide.md
# Index: 1
# Runnable: True
# Hash: b3fbebe3

# Python API usage
from src.controllers.factory import create_controller
from src.core.simulation_runner import run_simulation

# Create controller
controller = create_controller(
    'classical_smc',
    gains=[10.0, 8.0, 15.0, 12.0, 50.0, 5.0],
    max_force=100.0
)

# Run simulation
results = run_simulation(
    controller=controller,
    duration=10.0,
    dt=0.01,
    plot=True
)

# Analyze performance
print(f"Settling time: {results.metrics.settling_time:.2f}s")
print(f"Overshoot: {results.metrics.overshoot:.1f}%")
print(f"Control effort: {results.metrics.control_effort:.2f}N²")