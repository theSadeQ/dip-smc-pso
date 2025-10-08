# Example from: docs\reference\benchmarks\statistical_benchmarks_v2.md
# Index: 3
# Runnable: True
# Hash: 7145987c

from src.benchmarks.statistical_benchmarks_v2 import compare_controllers

# Define two controllers
def classical_factory():
    return create_smc_for_pso(SMCType.CLASSICAL, [10, 8, 15, 12, 50, 5])

def adaptive_factory():
    return create_smc_for_pso(SMCType.ADAPTIVE, [10, 8, 15, 12, 0.5])

# Statistical comparison
comparison = compare_controllers(
    controller_a_factory=classical_factory,
    controller_b_factory=adaptive_factory,
    config=config,
    n_trials=40
)

# Interpret results
for metric, result in comparison.items():
    print(f"
{metric.upper()}:")
    print(f"  Classical: {result['mean_a']:.4f} ± {result['std_a']:.4f}")
    print(f"  Adaptive:  {result['mean_b']:.4f} ± {result['std_b']:.4f}")
    print(f"  p-value:   {result['p_value']:.4e}")

    if result['p_value'] < 0.05:
        better = 'Classical' if result['mean_a'] < result['mean_b'] else 'Adaptive'
        print(f"  → {better} is significantly better (p < 0.05)")
    else:
        print(f"  → No significant difference (p ≥ 0.05)")