# Example from: docs\reference\utils\reproducibility___init__.md
# Index: 5
# Runnable: True
# Hash: 3622c6a3

from src.utils.reproducibility import set_seed, capture_random_state
import json
from pathlib import Path

class ReproducibleExperiment:
    def __init__(self, name: str, seed: int):
        self.name = name
        self.seed = seed
        set_seed(seed)
        self.initial_state = capture_random_state()

    def run(self):
        # Restore initial state for clean run
        restore_random_state(self.initial_state)

        # Run experiment
        results = self.execute_experiment()

        # Save results with metadata
        self.save_results(results)

        return results

    def save_results(self, results):
        metadata = {
            'experiment': self.name,
            'seed': self.seed,
            'results': results
        }

        Path('results').mkdir(exist_ok=True)
        with open(f'results/{self.name}_seed{self.seed}.json', 'w') as f:
            json.dump(metadata, f, indent=2)

# Run reproducible experiment
exp = ReproducibleExperiment("controller_comparison", seed=42)
results = exp.run()

# Re-run with same seed - identical results guaranteed
exp2 = ReproducibleExperiment("controller_comparison", seed=42)
results2 = exp2.run()

assert results == results2
print("✓ Full experiment reproducibility achieved")