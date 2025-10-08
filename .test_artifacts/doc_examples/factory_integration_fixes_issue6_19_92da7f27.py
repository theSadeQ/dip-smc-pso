# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 19
# Runnable: True
# Hash: 92da7f27

from src.optimization.integration.pso_factory_bridge import (
    optimize_classical_smc, optimize_adaptive_smc, optimize_sta_smc
)

# One-line optimization for each controller type
classical_factory, classical_result = optimize_classical_smc()
adaptive_factory, adaptive_result = optimize_adaptive_smc()
sta_factory, sta_result = optimize_sta_smc()

# Use optimized controllers
classical_controller = classical_factory()  # Uses optimized gains
adaptive_controller = adaptive_factory()
sta_controller = sta_factory()