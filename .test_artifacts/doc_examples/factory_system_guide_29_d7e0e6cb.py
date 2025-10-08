# Example from: docs\controllers\factory_system_guide.md
# Index: 29
# Runnable: False
# Hash: d7e0e6cb

# 1. Use create_pso_controller_factory for consistent interface
factory = create_pso_controller_factory(SMCType.CLASSICAL, max_force=100.0, dt=0.01)

# 2. Validate gains before PSO evaluation
valid_mask = np.array([validate_smc_gains(SMCType.CLASSICAL, gains) for gains in particles])
costs[~valid_mask] = PENALTY_VALUE

# 3. Use appropriate bounds for each controller type
lower_bounds, upper_bounds = get_gain_bounds_for_pso(SMCType.CLASSICAL)

# 4. Add controller-specific constraints to PSO validation
if smc_type == SMCType.SUPER_TWISTING:
    K1, K2 = gains[0], gains[1]
    if K1 <= K2:
        return False  # Violates stability constraint