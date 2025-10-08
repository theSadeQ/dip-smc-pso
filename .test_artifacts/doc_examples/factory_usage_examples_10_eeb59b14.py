# Example from: docs\technical\factory_usage_examples.md
# Index: 10
# Runnable: True
# Hash: eeb59b14

from src.optimization.integration.pso_factory_bridge import (
    optimize_classical_smc, optimize_adaptive_smc, optimize_sta_smc
)

# Quick optimization for each controller type
classical_factory, classical_result = optimize_classical_smc()
adaptive_factory, adaptive_result = optimize_adaptive_smc()
sta_factory, sta_result = optimize_sta_smc()

# Use optimized controllers immediately
classical_controller = classical_factory()  # Uses optimized gains
adaptive_controller = adaptive_factory()
sta_controller = sta_factory()

# Access optimization results
print(f"Classical optimization cost: {classical_result['best_cost']:.6f}")
print(f"Adaptive optimization cost: {adaptive_result['best_cost']:.6f}")
print(f"STA optimization cost: {sta_result['best_cost']:.6f}")