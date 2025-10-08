# Example from: docs\guides\workflows\batch-simulation-workflow.md
# Index: 2
# Runnable: True
# Hash: eb59a47d

from src.simulation.orchestrators.batch import BatchOrchestrator
from src.controllers.factory import create_controller
import numpy as np

# Initialize orchestrator
orchestrator = BatchOrchestrator()

# Batch execution
batch_size = 50
initial_states = np.random.normal(0, 0.1, (batch_size, 6))
controls = np.zeros((batch_size, 500))

result_container = orchestrator.execute(
    initial_state=initial_states,
    control_inputs=controls,
    dt=0.01,
    horizon=500,
    safety_guards=True,  # Enable per-simulation guards
    stop_fn=None         # Optional early stopping
)

# Access results
states = result_container.get_states()  # (batch_size, 501, 6)
times = result_container.get_times()    # (501,)