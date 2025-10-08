# Example from: docs\reference\benchmarks\statistical_benchmarks_v2.md
# Index: 4
# Runnable: True
# Hash: 57117aee

from src.benchmarks.core import run_multiple_trials

controllers = {
    'Classical': lambda: create_smc_for_pso(SMCType.CLASSICAL, [10, 8, 15, 12, 50, 5]),
    'Adaptive': lambda: create_smc_for_pso(SMCType.ADAPTIVE, [10, 8, 15, 12, 0.5]),
    'STA': lambda: create_smc_for_pso(SMCType.SUPER_TWISTING, [25, 10, 15, 12, 20, 15]),
    'Hybrid': lambda: create_smc_for_pso(SMCType.HYBRID, [15, 12, 18, 15])
}

results = {}
for name, factory in controllers.items():
    metrics_list, ci_results = run_trials(factory, config, n_trials=30)
    results[name] = ci_results

# Compare ISE across all controllers
import pandas as pd
comparison_df = pd.DataFrame({
    name: {
        'ISE': r['ise']['mean'],
        'ISE_CI': f"[{r['ise']['ci_lower']:.3f}, {r['ise']['ci_upper']:.3f}]",
        'Settling Time': r['settling_time']['mean']
    }
    for name, r in results.items()
}).T

print(comparison_df)