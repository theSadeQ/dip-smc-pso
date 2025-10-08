# Example from: docs\testing\benchmarking_framework_technical_guide.md
# Index: 13
# Runnable: True
# Hash: 0003d32a

# Example 1: Basic controller benchmarking
from src.benchmarks import run_trials
from src.controllers.smc.classic_smc import ClassicalSMC

metrics_list, ci_results = run_trials(
    controller_factory=lambda: ClassicalSMC(
        gains=[10, 8, 15, 12, 50, 5],
        max_force=100,
        boundary_layer=0.01
    ),
    cfg=config,
    n_trials=30,
    seed=42
)

for metric, stats in ci_results.items():
    print(f"{metric}: {stats['mean']:.4f} ± {stats['ci_width']:.4f}")

# Example 2: Controller comparison
from src.benchmarks import compare_controllers

comparison = compare_controllers(
    controller_a_factory=lambda: ClassicalSMC(gains=[10,8,15,12,50,5], max_force=100),
    controller_b_factory=lambda: AdaptiveSMC(gains=[10,8,15,12,0.5], max_force=100),
    cfg=config,
    n_trials=30,
    metric='ise'
)

if comparison['significant']:
    print(f"Controller {comparison['better_controller']} is significantly better (p={comparison['p_value']:.4f})")