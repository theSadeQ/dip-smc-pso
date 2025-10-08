# Example from: docs\reference\simulation\engines_simulation_runner.md
# Index: 4
# Runnable: True
# Hash: 2b1936c4

from src.simulation.engines.simulation_runner import run_simulation

# Compare Euler vs RK4 accuracy
methods = ['euler', 'rk4', 'rk45']
results = {}

for method in methods:
    result = run_simulation(
        controller=controller,
        dynamics=dynamics,
        initial_state=[0.1, 0.05, 0, 0, 0, 0],
        duration=10.0,
        dt=0.01,
        integration_method=method
    )
    results[method] = result

    # Analyze energy conservation
    energy_drift = np.abs(result.energy[-1] - result.energy[0])
    print(f"{method.upper()}: Energy drift = {energy_drift:.6f}")