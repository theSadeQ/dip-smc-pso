# Example from: docs\technical\factory_usage_examples.md
# Index: 20
# Runnable: False
# Hash: fbf6e12b

# example-metadata:
# runnable: false

"""Complete research workflow for controller comparison."""
from src.controllers.factory import create_controller
from src.optimization.integration.pso_factory_bridge import optimize_classical_smc, optimize_sta_smc

# Step 1: Create baseline controllers
baseline_controllers = {
    'classical': create_controller('classical_smc', gains=[8.0, 6.0, 4.0, 3.0, 15.0, 2.0]),
    'sta': create_controller('sta_smc', gains=[8.0, 4.0, 12.0, 6.0, 4.85, 3.43])
}

# Step 2: Optimize controllers
print("Optimizing controllers...")
classical_factory, classical_result = optimize_classical_smc()
sta_factory, sta_result = optimize_sta_smc()

optimized_controllers = {
    'classical_opt': classical_factory(),
    'sta_opt': sta_factory()
}

# Step 3: Compare performance
print("\nPerformance Comparison:")
print(f"Classical baseline vs optimized:")
print(f"  Optimized cost: {classical_result['best_cost']:.6f}")
print(f"  Optimized gains: {classical_result['best_gains']}")

print(f"\nSTA baseline vs optimized:")
print(f"  Optimized cost: {sta_result['best_cost']:.6f}")
print(f"  Optimized gains: {sta_result['best_gains']}")