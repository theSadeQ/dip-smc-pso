# Example from: docs\factory\configuration_migration_mathematical_foundations.md
# Index: 3
# Runnable: False
# Hash: 2b80d30c

# example-metadata:
# runnable: false

def migrate_sta_smc_parameters_mathematical(old_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mathematically sound migration for Super-Twisting SMC parameters.

    Mathematical Validation:
    1. Preserve finite-time convergence conditions
    2. Maintain super-twisting stability requirements
    3. Ensure proper algorithmic gain relationships
    """

    new_params = {}

    # Extract separate K1, K2 parameters (old format)
    K1 = old_params.get('K1', 0.0)
    K2 = old_params.get('K2', 0.0)
    old_gains = old_params.get('gains', [])

    # Mathematical migration: separate K1,K2 + surface gains → unified gains array
    if K1 > 0 and K2 > 0:
        # Validate super-twisting convergence conditions
        alpha = old_params.get('alpha_power', 0.5)

        # Simplified convergence check (assumes L=1 for typical systems)
        L_estimate = 1.0
        min_K1 = L_estimate / alpha
        min_K2 = K1**2 / (2 * L_estimate) + L_estimate

        if K1 < min_K1:
            print(f"Warning: K₁={K1:.2f} may be too small for convergence (min: {min_K1:.2f})")

        if K2 < min_K2:
            print(f"Warning: K₂={K2:.2f} may be too small for convergence (min: {min_K2:.2f})")

        # Extract surface gains or use defaults
        if len(old_gains) >= 4:
            k1, k2, lam1, lam2 = old_gains[:4]
        else:
            # Default surface gains for double pendulum
            k1, k2, lam1, lam2 = 20.0, 15.0, 12.0, 8.0

        # Validate surface gain positivity
        if any(g <= 0 for g in [k1, k2, lam1, lam2]):
            raise ValueError("All surface gains must be positive")

        # Create unified gains array: [K1, K2, k1, k2, λ1, λ2]
        new_params['gains'] = [K1, K2, k1, k2, lam1, lam2]

    elif len(old_gains) >= 6:
        # Already in new format, validate convergence conditions
        K1, K2, k1, k2, lam1, lam2 = old_gains[:6]

        # Validate all gains are positive
        if any(g <= 0 for g in [K1, K2, k1, k2, lam1, lam2]):
            raise ValueError("All STA-SMC gains must be positive")

        new_params['gains'] = [K1, K2, k1, k2, lam1, lam2]

    # Migrate algorithm-specific parameters
    algorithm_mappings = {
        'alpha_power': 'power_exponent',
        'switching_function_type': 'switch_method',
        'regularization_parameter': 'regularization'
    }

    for old_param, new_param in algorithm_mappings.items():
        if old_param in old_params:
            new_params[new_param] = old_params[old_param]

    # Ensure algorithm parameters with mathematical justification
    power_exp = new_params.get('power_exponent', 0.5)
    if not (0 < power_exp < 1):
        raise ValueError(f"Power exponent α={power_exp} must be in (0,1) for finite-time convergence")

    new_params.setdefault('power_exponent', 0.5)  # Optimal for most systems
    new_params.setdefault('regularization', 1e-6)  # Numerical stability
    new_params.setdefault('boundary_layer', 0.01)  # Small boundary for STA
    new_params.setdefault('switch_method', 'tanh')  # Smooth switching
    new_params.setdefault('damping_gain', 0.0)  # No additional damping by default

    # Advanced validation: Check Lyapunov function decrease rate
    if 'gains' in new_params and len(new_params['gains']) >= 6:
        K1, K2 = new_params['gains'][:2]
        alpha = new_params['power_exponent']

        # Estimate convergence time (simplified analysis)
        T_convergence = 2 * (1 / (1 - alpha)) * (1 / min(K1, K2)**0.5)
        if T_convergence > 10.0:  # More than 10 seconds
            print(f"Warning: Estimated convergence time {T_convergence:.2f}s may be too slow")

    return new_params

# Mathematical validation example
old_sta_config = {
    'K1': 35.0,
    'K2': 20.0,
    'gains': [25.0, 18.0, 12.0, 8.0],  # Surface gains
    'alpha_power': 0.5,
    'switching_function_type': 'tanh',
    'regularization_parameter': 1e-6
}

migrated_config = migrate_sta_smc_parameters_mathematical(old_sta_config)
print("Migrated STA-SMC config:", migrated_config)