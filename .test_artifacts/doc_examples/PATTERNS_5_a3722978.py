# Example from: docs\PATTERNS.md
# Index: 5
# Runnable: True
# Hash: a3722978

# Client code selects strategy at runtime
if analysis_type == 'monte_carlo':
    strategy = MonteCarloStrategy(n_samples=1000)
elif analysis_type == 'sensitivity':
    strategy = SensitivityAnalysisStrategy(perturbation=0.01)

# Execute with chosen strategy
results = strategy.analyze(simulation_fn, parameters)