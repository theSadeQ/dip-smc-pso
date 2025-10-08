# Example from: docs\factory\configuration_migration_mathematical_foundations.md
# Index: 2
# Runnable: False
# Hash: aa314d9d

# example-metadata:
# runnable: false

def migrate_adaptive_smc_parameters_mathematical(old_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mathematically sound migration for Adaptive SMC parameters.

    Mathematical Validation:
    1. Preserve adaptation law stability
    2. Maintain Lyapunov convergence conditions
    3. Ensure bounded parameter estimates
    """

    new_params = {}

    # Extract old parameter structure
    old_gains = old_params.get('gains', [])
    adaptation_gain = old_params.get('adaptation_gain', 0.0)

    # Mathematical migration: [k1, k2, λ1, λ2] + γ → [k1, k2, λ1, λ2, γ]
    if len(old_gains) == 4:
        k1, k2, lam1, lam2 = old_gains

        # Validate stability conditions
        if lam1 <= 0 or lam2 <= 0:
            raise ValueError("Sliding surface coefficients λ₁, λ₂ must be positive")

        if k1 <= 0 or k2 <= 0:
            raise ValueError("Proportional gains k₁, k₂ must be positive")

        # Use provided adaptation gain or calculate from stability requirements
        if adaptation_gain > 0:
            gamma = adaptation_gain
        else:
            # Calculate adaptation gain from stability margin
            # γ should be large enough for fast adaptation but not cause oscillations
            gamma = min(k1, k2) * 0.5  # Conservative choice

        # Validate adaptation rate bounds
        if gamma <= 0:
            raise ValueError("Adaptation rate γ must be positive for convergence")

        if gamma > 20.0:  # Practical upper bound
            print(f"Warning: High adaptation rate γ={gamma:.2f} may cause oscillations")

        new_params['gains'] = [k1, k2, lam1, lam2, gamma]

    # Migration of adaptation parameters
    adaptation_mappings = {
        'boundary_layer_thickness': 'boundary_layer',
        'estimate_bounds': ('K_min', 'K_max'),  # Special case: split parameter
        'adaptation_law': 'alpha',
        'leak_coefficient': 'leak_rate'
    }

    for old_param, new_param in adaptation_mappings.items():
        if old_param in old_params:
            if old_param == 'estimate_bounds':
                # Split bounds into separate parameters
                bounds = old_params[old_param]
                if isinstance(bounds, (list, tuple)) and len(bounds) == 2:
                    new_params['K_min'] = bounds[0]
                    new_params['K_max'] = bounds[1]

                    # Validate bounds
                    if new_params['K_min'] >= new_params['K_max']:
                        raise ValueError("K_min must be less than K_max")
                    if new_params['K_min'] <= 0:
                        raise ValueError("K_min must be positive")
            else:
                new_params[new_param] = old_params[old_param]

    # Ensure required adaptation parameters with theoretical justification
    new_params.setdefault('leak_rate', 0.01)  # 1% leak rate prevents drift
    new_params.setdefault('K_min', 0.1)  # Minimum for controllability
    new_params.setdefault('K_max', 100.0)  # Maximum for actuator limits
    new_params.setdefault('adapt_rate_limit', 10.0)  # Prevent excessive adaptation
    new_params.setdefault('alpha', 0.5)  # Compromise between speed and stability
    new_params.setdefault('dead_zone', 0.05)  # Noise tolerance
    new_params.setdefault('boundary_layer', 0.01)  # Smaller for adaptation
    new_params.setdefault('smooth_switch', True)  # Reduce chattering

    # Validate adaptation stability conditions
    if 'gains' in new_params and len(new_params['gains']) >= 5:
        gamma = new_params['gains'][4]
        leak_rate = new_params['leak_rate']

        # Check adaptation stability: σ/γ should be small for good tracking
        stability_ratio = leak_rate / gamma
        if stability_ratio > 0.1:
            print(f"Warning: High leak-to-adaptation ratio {stability_ratio:.3f} may degrade performance")

    return new_params

# Mathematical validation example
old_adaptive_config = {
    'gains': [25.0, 18.0, 15.0, 10.0],  # [k1, k2, λ1, λ2]
    'adaptation_gain': 4.0,
    'boundary_layer_thickness': 0.02,
    'estimate_bounds': [0.1, 100.0],
    'adaptation_law': 0.5
}

migrated_config = migrate_adaptive_smc_parameters_mathematical(old_adaptive_config)
print("Migrated Adaptive SMC config:", migrated_config)