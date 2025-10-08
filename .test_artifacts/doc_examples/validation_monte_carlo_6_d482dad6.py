# Example from: docs\reference\analysis\validation_monte_carlo.md
# Index: 6
# Runnable: True
# Hash: d482dad6

from src.analysis.validation.monte_carlo import MonteCarloValidator
from src.controllers.factory import create_smc_for_pso, SMCType

# Define controller
controller_factory = lambda: create_smc_for_pso(
    SMCType.CLASSICAL,
    gains=[10, 8, 15, 12, 50, 5],
    max_force=100.0
)

# Configure uncertainty model (±20% on masses, ±10% on lengths)
uncertainty = {
    'cart_mass': {'type': 'uniform', 'range': (-0.2, 0.2)},
    'pole1_mass': {'type': 'uniform', 'range': (-0.2, 0.2)},
    'pole2_mass': {'type': 'uniform', 'range': (-0.2, 0.2)},
    'pole1_length': {'type': 'uniform', 'range': (-0.1, 0.1)},
    'pole2_length': {'type': 'uniform', 'range': (-0.1, 0.1)},
}

# Run Monte Carlo validation
validator = MonteCarloValidator(
    controller_factory=controller_factory,
    uncertainty_model=uncertainty,
    n_samples=100,
    seed=42
)

results = validator.run()

# Analyze robustness
print(f"Success Rate: {results['success_rate']*100:.1f}%")
print(f"Mean ISE: {results['mean_ise']:.4f}")
print(f"Worst-case ISE: {results['worst_case_ise']:.4f}")
print(f"95th Percentile ISE: {results['percentile_95_ise']:.4f}")