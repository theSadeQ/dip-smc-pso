# Example from: docs\api\simulation_engine_api_reference.md
# Index: 45
# Runnable: True
# Hash: 38bca3fc

from src.simulation.orchestrators import SequentialOrchestrator
from src.simulation.integrators import IntegratorFactory

# Create orchestrator
integrator = IntegratorFactory.create_integrator('rk4', dt=0.01)
orchestrator = SequentialOrchestrator(dynamics, integrator)

# Execute simulation
initial_state = np.array([0, 0.1, 0.1, 0, 0, 0])
controls = controller_sequence  # (horizon,) array
result = orchestrator.execute(
    initial_state=initial_state,
    control_inputs=controls,
    dt=0.01,
    horizon=500,
    safety_guards=True
)

# Access results
states = result.get_states()   # (horizon+1, 6)
times = result.get_times()     # (horizon+1,)