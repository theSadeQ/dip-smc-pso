# Example from: docs\guides\workflows\batch-simulation-workflow.md
# Index: 12
# Runnable: True
# Hash: dd5ce851

# Vector simulation
from src.simulation.engines.vector_sim import simulate
results = simulate(initial_states, controls, dt, horizon, **options)

# Batch orchestrator
from src.simulation.orchestrators.batch import BatchOrchestrator
orchestrator = BatchOrchestrator()
container = orchestrator.execute(initial_state, control_inputs, dt, horizon, **kwargs)

# Result containers
from src.simulation.results.containers import BatchResultContainer
states = container.get_states(batch_index=None)  # All or specific trial
times = container.get_times(batch_index=None)
count = container.get_batch_count()