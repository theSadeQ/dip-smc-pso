# Example from: docs\reference\analysis\validation_monte_carlo.md
# Index: 4
# Runnable: True
# Hash: f0d4b49d

# Analyze multiple trials
results = []
for trial in range(n_trials):
    result = run_simulation(trial_seed=trial)
    results.append(analyzer.analyze(result))

# Aggregate statistics
mean_performance = np.mean([r.performance for r in results])