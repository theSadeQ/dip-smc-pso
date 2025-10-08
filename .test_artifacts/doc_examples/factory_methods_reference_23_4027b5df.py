# Example from: docs\api\factory_methods_reference.md
# Index: 23
# Runnable: False
# Hash: 4027b5df

# Get bounds for PSO optimization
bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)
lower_bounds, upper_bounds = bounds

print(f"Lower bounds: {lower_bounds}")
print(f"Upper bounds: {upper_bounds}")

# Use with PSO optimizer
pso_config = {
    'bounds': bounds,
    'n_particles': 30,
    'max_iter': 100
}

# Validate bounds make sense
assert len(lower_bounds) == 6  # Classical SMC has 6 gains
assert all(l < u for l, u in zip(lower_bounds, upper_bounds))