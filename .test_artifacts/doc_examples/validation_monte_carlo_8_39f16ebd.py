# Example from: docs\reference\analysis\validation_monte_carlo.md
# Index: 8
# Runnable: True
# Hash: 39f16ebd

from src.analysis.validation.monte_carlo import LatinHypercubeSampler

# High-dimensional uncertainty (all 8 physics parameters)
uncertainty_full = {
    'cart_mass': (-0.2, 0.2),
    'pole1_mass': (-0.2, 0.2),
    'pole2_mass': (-0.2, 0.2),
    'pole1_length': (-0.1, 0.1),
    'pole2_length': (-0.1, 0.1),
    'friction_cart': (-0.3, 0.3),
    'friction_pole1': (-0.3, 0.3),
    'friction_pole2': (-0.3, 0.3),
}

# Latin Hypercube Sampling (more efficient than random for high dimensions)
sampler = LatinHypercubeSampler(uncertainty_full, n_samples=150, seed=42)
param_samples = sampler.generate()

# Run validation with LHS samples
validator = MonteCarloValidator(
    controller_factory=controller_factory,
    param_samples=param_samples  # Pre-generated samples
)

results = validator.run()

# Analyze which parameters drive failures
failure_params = param_samples[~results['stability_mask']]
print(f"Failure modes analysis:")
print(f"  Cart mass range in failures: [{failure_params[:, 0].min():.3f}, {failure_params[:, 0].max():.3f}]")
print(f"  Pole1 length range in failures: [{failure_params[:, 3].min():.3f}, {failure_params[:, 3].max():.3f}]")