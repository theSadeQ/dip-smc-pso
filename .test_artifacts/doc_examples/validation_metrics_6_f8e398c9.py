# Example from: docs\reference\analysis\validation_metrics.md
# Index: 6
# Runnable: True
# Hash: f8e398c9

from src.benchmarks.metrics import compute_all_metrics
from src.simulation.engines.simulation_runner import run_simulation
from src.controllers.factory import create_smc_for_pso, SMCType
from src.plant.models.simplified import SimplifiedDynamics

# Run simulation
controller = create_smc_for_pso(SMCType.CLASSICAL, [10, 8, 15, 12, 50, 5])
dynamics = SimplifiedDynamics()

result = run_simulation(
    controller=controller,
    dynamics_model=dynamics,
    initial_state=[0.1, 0.05, 0, 0, 0, 0],
    sim_time=10.0,
    dt=0.01
)

# Compute comprehensive metrics
metrics = compute_all_metrics(
    t=result.time,
    x=result.states,
    u=result.control,
    max_force=100.0,
    include_advanced=True
)

# Access metrics
print("Control Performance:")
print(f"  ISE: {metrics['ise']:.4f}")
print(f"  ITAE: {metrics['itae']:.4f}")
print(f"  RMS Control: {metrics['rms_control']:.4f}")

print("
Stability Analysis:")
print(f"  Settling Time: {metrics['settling_time']:.3f}s")
print(f"  Overshoot: {metrics['overshoot']:.2f}%")
print(f"  Damping Ratio: {metrics['damping_ratio']:.3f}")

print("
Constraint Violations:")
print(f"  Saturation Count: {metrics['saturation_count']}")
print(f"  Saturation Severity: {metrics['saturation_severity']:.4f}")