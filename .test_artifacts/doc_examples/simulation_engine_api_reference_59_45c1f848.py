# Example from: docs\api\simulation_engine_api_reference.md
# Index: 59
# Runnable: True
# Hash: 45c1f848

from src.simulation.integrators import IntegratorFactory

# High-accuracy integration
dp45 = IntegratorFactory.create_integrator(
    'dp45',
    dt=0.01,
    atol=1e-8,   # Tight tolerance
    rtol=1e-6
)

# Use with orchestrator
orchestrator = SequentialOrchestrator(dynamics, dp45)
result = orchestrator.execute(
    initial_state=x0,
    control_inputs=controls,
    dt=0.01,  # Initial dt (will adapt)
    horizon=1000
)

# Check integration statistics
stats = dp45.get_statistics()
print(f"Accepted steps: {stats['accepted_steps']}")
print(f"Rejected steps: {stats['rejected_steps']}")
print(f"Average step size: {stats['mean_step_size']:.4f}s")