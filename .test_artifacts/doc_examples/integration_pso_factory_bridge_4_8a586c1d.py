# Example from: docs\reference\optimization\integration_pso_factory_bridge.md
# Index: 4
# Runnable: True
# Hash: 8a586c1d

# Use in complete optimization loop
optimizer = create_optimizer(opt_type, config)
result = optimize(optimizer, problem, max_iter=100)