# Example from: docs\mathematical_foundations\simulation_architecture_guide.md
# Index: 14
# Runnable: True
# Hash: 0fe278de

from src.simulation.orchestrators.batch import BatchOrchestrator
import numpy as np

orchestrator = BatchOrchestrator()

# Batch initial conditions (Monte Carlo)
n_runs = 100
x0_batch = np.random.randn(n_runs, 6) * 0.1
u_batch = np.zeros((n_runs, 1000))

result = orchestrator.execute(
    initial_state=x0_batch,
    control_inputs=u_batch,
    dt=0.01,
    horizon=1000,
    safety_guards=True,
    stop_fn=lambda x: abs(x[1]) > np.pi/2
)

# Access results
print(f"Batch size: {result.batch_size}")
print(f"Successful runs: {result.success_count}")
print(f"Execution time: {result.execution_time:.3f}s")