# Example from: docs\reference\optimization\algorithms_gradient_based_bfgs.md
# Index: 3
# Runnable: True
# Hash: 8a586c1d

# Use in complete optimization loop
optimizer = create_optimizer(opt_type, config)
result = optimize(optimizer, problem, max_iter=100)