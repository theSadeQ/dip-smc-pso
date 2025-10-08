# Example from: docs\plant\models_guide.md
# Index: 20
# Runnable: False
# Hash: 5ed51cc7

# example-metadata:
# runnable: false

from src.plant.models.simplified import SimplifiedDIPDynamics
from src.plant.models.full import FullDIPDynamics
from src.plant.models.lowrank import LowRankDIPDynamics
import time

# Create all three models with same configuration
config_dict = {
    'cart_mass': 1.0,
    'pendulum1_mass': 0.1,
    'pendulum2_mass': 0.1,
    # ... (same parameters for all)
}

simplified = SimplifiedDIPDynamics(config_dict, enable_fast_mode=True)
full = FullDIPDynamics(config_dict)
lowrank = LowRankDIPDynamics(config_dict)

# Test state
state = np.array([0.0, 0.1, -0.05, 0.0, 0.0, 0.0])
control = np.array([5.0])

# Benchmark computation time
models = [('Simplified', simplified), ('Full', full), ('Low-Rank', lowrank)]

for name, model in models:
    start = time.perf_counter()
    for _ in range(1000):
        result = model.compute_dynamics(state, control)
    elapsed = time.perf_counter() - start

    print(f"{name:12s}: {elapsed*1000:.2f} ms (1000 evaluations)")
    print(f"  Energy: {result.info.get('total_energy', 0.0):.6f} J")