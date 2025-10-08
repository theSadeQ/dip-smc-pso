# Example from: docs\benchmarks_methodology.md
# Index: 8
# Runnable: True
# Hash: 7cf32c05

uncertainty_levels = [0.0, 0.05, 0.10, 0.15, 0.20]
sensitivity_results = {}

for uncertainty in uncertainty_levels:
    # Update config with uncertainty level
    config.physics_uncertainty.cart_mass = uncertainty

    # Run benchmark
    _, ci_results = run_trials(factory, config, n_trials=30)
    sensitivity_results[uncertainty] = ci_results['ise'][0]  # Mean ISE