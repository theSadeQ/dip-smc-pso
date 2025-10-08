# Example from: docs\technical\pso_integration_workflows.md
# Index: 6
# Runnable: False
# Hash: d366a770

from src.optimization.integration.pso_factory_bridge import (
    optimize_classical_smc, optimize_adaptive_smc, optimize_sta_smc
)

# Quick optimization for each controller type
print("Optimizing controllers...")

classical_factory, classical_result = optimize_classical_smc()
adaptive_factory, adaptive_result = optimize_adaptive_smc()
sta_factory, sta_result = optimize_sta_smc()

# Compare optimization results
results = {
    'Classical SMC': classical_result['best_cost'],
    'Adaptive SMC': adaptive_result['best_cost'],
    'STA SMC': sta_result['best_cost']
}

print("\nOptimization Results:")
for controller, cost in results.items():
    print(f"  {controller}: {cost:.6f}")

# Use optimized controllers
optimized_controllers = {
    'classical': classical_factory(),
    'adaptive': adaptive_factory(),
    'sta': sta_factory()
}