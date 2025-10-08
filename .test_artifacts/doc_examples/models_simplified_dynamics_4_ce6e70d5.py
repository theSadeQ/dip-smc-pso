# Example from: docs\reference\plant\models_simplified_dynamics.md
# Index: 4
# Runnable: True
# Hash: ce6e70d5

from src.plant.models import SimplifiedDynamics, FullDynamics, LowRankDynamics

models = {
    'Simplified': SimplifiedDynamics(),
    'Full': FullDynamics(),
    'LowRank': LowRankDynamics()
}

# Compare computational cost
import time
state = [0.1, 0.2, 0.1, 0, 0, 0]
control = 10.0

for name, model in models.items():
    start = time.perf_counter()
    for _ in range(10000):
        model.compute_dynamics(state, control, 0)
    elapsed = time.perf_counter() - start

    print(f"{name}: {elapsed*1000:.2f}ms for 10k evaluations")
    print(f"  → {elapsed/10000*1e6:.2f}µs per call")