"""Quick script to test adaptive inertia PSO with manual w_schedule."""
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from src.config import load_config
from src.controllers.factory import create_controller
from src.optimization.algorithms.pso_optimizer import PSOTuner

# Load config
config_path = Path(__file__).parent.parent.parent.parent.parent / "config.yaml"
config = load_config(str(config_path), allow_unknown=True)

# Manually set w_schedule as tuple (bypass YAML validation)
config.pso.w_schedule = (0.9, 0.4)

# Create controller factory
def controller_factory(gains):
    return create_controller(
        'classical_smc',
        config=config.controllers.classical_smc,
        gains=gains
    )

# Create PSO tuner
tuner = PSOTuner(
    controller_factory=controller_factory,
    config=config,
    seed=42
)

print("Running PSO with adaptive inertia (w: 0.9 → 0.4)...")
print(f"Iterations: {config.pso.iters}")
print(f"Particles: {config.pso.n_particles}")
print()

# Run optimization
import time
start_time = time.time()
result = tuner.optimise()
wall_time = time.time() - start_time

print(f"\nOptimization Complete:")
print(f"  Best Cost: {result['best_cost']:.6f}")
print(f"  Best Gains: {result['best_pos']}")
print(f"  Wall Time: {wall_time:.2f} seconds")

# Save gains
output_path = Path(__file__).parent / "gains_adaptive_inertia.json"
with open(output_path, 'w') as f:
    json.dump({"classical_smc": result['best_pos'].tolist()}, f, indent=2)
print(f"\nGains saved to: {output_path}")

# Save metrics
metrics = {
    "method": "adaptive_inertia",
    "w_schedule": [0.9, 0.4],
    "iterations": config.pso.iters,
    "best_cost": float(result['best_cost']),
    "wall_time_seconds": wall_time,
    "best_gains": result['best_pos'].tolist()
}

metrics_path = Path(__file__).parent / "adaptive_metrics.json"
with open(metrics_path, 'w') as f:
    json.dump(metrics, f, indent=2)
print(f"Metrics saved to: {metrics_path}")
