# Example from: docs\PATTERNS.md
# Index: 9
# Runnable: False
# Hash: 733c3739

# Legacy controller
legacy_controller = ClassicalSMC(gains=[...])

# Wrap for PSO compatibility
pso_compatible = PSOControllerWrapper(legacy_controller, n_gains=6,
                                      controller_type='classical_smc')

# Now works with PSO optimizer
optimizer.optimize(pso_compatible.compute_control)