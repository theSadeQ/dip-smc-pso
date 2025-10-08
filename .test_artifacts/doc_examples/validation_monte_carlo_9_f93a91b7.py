# Example from: docs\reference\analysis\validation_monte_carlo.md
# Index: 9
# Runnable: False
# Hash: f93a91b7

# example-metadata:
# runnable: false

controllers = {
    'Classical': lambda: create_smc_for_pso(SMCType.CLASSICAL, [10, 8, 15, 12, 50, 5]),
    'Adaptive': lambda: create_smc_for_pso(SMCType.ADAPTIVE, [10, 8, 15, 12, 0.5]),
}

uncertainty = {
    'cart_mass': {'type': 'uniform', 'range': (-0.3, 0.3)},  # Aggressive uncertainty
    'pole1_mass': {'type': 'uniform', 'range': (-0.3, 0.3)},
}

robustness_results = {}
for name, factory in controllers.items():
    validator = MonteCarloValidator(factory, uncertainty, n_samples=200)
    robustness_results[name] = validator.run()

# Compare success rates
for name, res in robustness_results.items():
    print(f"{name}:")
    print(f"  Success Rate: {res['success_rate']*100:.1f}%")
    print(f"  Mean ISE (successful): {res['mean_ise']:.4f}")
    print(f"  Worst-case ISE: {res['worst_case_ise']:.4f}")