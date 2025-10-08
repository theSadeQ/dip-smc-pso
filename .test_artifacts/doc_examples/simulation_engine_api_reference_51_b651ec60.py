# Example from: docs\api\simulation_engine_api_reference.md
# Index: 51
# Runnable: True
# Hash: b651ec60

from src.simulation.integrators import IntegratorFactory

# Create RK4 integrator
rk4 = IntegratorFactory.create_integrator('rk4', dt=0.01)

# Create adaptive integrator with error tolerances
dp45 = IntegratorFactory.create_integrator(
    'dormand_prince',
    dt=0.01,
    atol=1e-6,
    rtol=1e-3
)

# Use with orchestrator
from src.simulation.orchestrators import SequentialOrchestrator
orchestrator = SequentialOrchestrator(dynamics, rk4)