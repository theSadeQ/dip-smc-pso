# Example from: docs\benchmarks_methodology.md
# Index: 6
# Runnable: False
# Hash: bb278e7d

controllers = ['classical_smc', 'sta_smc', 'adaptive_smc']
results = {}

for ctrl_name in controllers:
    factory = create_controller_factory(ctrl_name, getattr(config.controllers, ctrl_name))
    _, ci_results = run_trials(factory, config, n_trials=30)
    results[ctrl_name] = ci_results

# Compare ISE performance
for ctrl, metrics in results.items():
    ise_mean, ise_ci = metrics['ise']
    print(f"{ctrl}: ISE = {ise_mean:.3f} ± {ise_ci:.3f}")