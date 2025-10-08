# Example from: docs\guides\api\simulation.md
# Index: 13
# Runnable: True
# Hash: fe798ada

from src.core.simulation_context import SimulationContext

context = SimulationContext(
    config=config,
    controller=controller,
    dynamics=dynamics,
    initial_state=np.array([0, 0, 0.1, 0, 0.15, 0])
)

# Context provides:
# - Consistent logging
# - Safety guards
# - Performance monitoring
# - Error recovery