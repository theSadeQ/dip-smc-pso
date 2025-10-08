# Example from: docs\api\simulation_engine_api_reference.md
# Index: 61
# Runnable: True
# Hash: f21275bf

zoh = IntegratorFactory.create_integrator('zoh', dt=0.01)

# Typical use with discrete controller
orchestrator = SequentialOrchestrator(dynamics, zoh)
result = orchestrator.execute(
    initial_state=x0,
    control_inputs=discrete_controls,  # Piecewise constant
    dt=0.01,
    horizon=500
)