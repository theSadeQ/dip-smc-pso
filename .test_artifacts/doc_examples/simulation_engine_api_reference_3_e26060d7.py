# Example from: docs\api\simulation_engine_api_reference.md
# Index: 3
# Runnable: True
# Hash: e26060d7

# Sequential execution
seq_orchestrator = SequentialOrchestrator(dynamics, integrator)
result = seq_orchestrator.execute(initial_state, controls, dt, horizon)

# Batch execution
batch_orchestrator = BatchOrchestrator(dynamics, integrator)
result = batch_orchestrator.execute(batch_initial_states, controls, dt, horizon)