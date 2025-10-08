# Example from: docs\factory\configuration_migration_mathematical_foundations.md
# Index: 4
# Runnable: False
# Hash: 7c9af2a8

def migrate_hybrid_smc_parameters_mathematical(old_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mathematically sound migration for Hybrid SMC parameters.

    Mathematical Validation:
    1. Preserve mode switching stability
    2. Maintain unified surface design
    3. Ensure sub-controller compatibility
    """

    new_params = {}

    # Extract surface gains (shared across all modes)
    surface_gains = old_params.get('gains', [18.0, 12.0, 10.0, 8.0])

    if len(surface_gains) != 4:
        raise ValueError("Hybrid SMC requires exactly 4 surface gains [c₁, λ₁, c₂, λ₂]")

    c1, lam1, c2, lam2 = surface_gains

    # Validate surface stability
    if any(g <= 0 for g in [c1, lam1, c2, lam2]):
        raise ValueError("All surface coefficients must be positive")

    # Check surface eigenvalue placement for stability
    eigen1 = -lam1 / c1
    eigen2 = -lam2 / c2
    if eigen1 >= 0 or eigen2 >= 0:
        print(f"Warning: Surface eigenvalues [{eigen1:.3f}, {eigen2:.3f}] may indicate instability")

    new_params['gains'] = surface_gains

    # Handle mode parameter migration
    mode_mappings = {
        'mode': 'hybrid_mode',
        'switch_threshold': 'switching_criteria',
        'classical_params': 'classical_config',
        'adaptive_params': 'adaptive_config'
    }

    for old_param, new_param in mode_mappings.items():
        if old_param in old_params:
            if old_param == 'switch_threshold':
                # Convert scalar threshold to criteria dict
                threshold = old_params[old_param]
                new_params['switching_criteria'] = {
                    'error_threshold': threshold,
                    'time_threshold': 2.0,  # Default time threshold
                    'performance_threshold': 0.1  # Performance-based switching
                }
            else:
                new_params[new_param] = old_params[old_param]

    # Handle sub-controller gain migration
    if 'sub_controller_gains' in old_params:
        sub_gains = old_params['sub_controller_gains']

        if isinstance(sub_gains, dict):
            # Create proper sub-controller configurations
            classical_gains = sub_gains.get('classical', [20.0, 15.0, 12.0, 8.0, 35.0, 5.0])
            adaptive_gains = sub_gains.get('adaptive', [25.0, 18.0, 15.0, 10.0, 4.0])

            # Validate sub-controller gains
            if len(classical_gains) != 6:
                raise ValueError("Classical sub-controller requires 6 gains")
            if len(adaptive_gains) != 5:
                raise ValueError("Adaptive sub-controller requires 5 gains")

            # Create complete sub-configurations with surface coupling
            new_params['classical_config'] = {
                'gains': classical_gains,
                'max_force': old_params.get('max_force', 150.0),
                'boundary_layer': 0.02,
                'dt': old_params.get('dt', 0.001),
                'surface_coupling': True  # Ensure surface consistency
            }

            new_params['adaptive_config'] = {
                'gains': adaptive_gains,
                'max_force': old_params.get('max_force', 150.0),
                'leak_rate': 0.01,
                'adapt_rate_limit': 10.0,
                'K_min': 0.1,
                'K_max': 100.0,
                'dt': old_params.get('dt', 0.001),
                'surface_coupling': True  # Ensure surface consistency
            }

    # Set hybrid-specific parameters with mathematical justification
    new_params.setdefault('hybrid_mode', 'CLASSICAL_ADAPTIVE')  # Conservative default
    new_params.setdefault('dt', 0.001)  # Fast sampling for mode switching
    new_params.setdefault('max_force', 150.0)  # Shared actuator limit

    # Advanced hybrid parameters
    new_params.setdefault('mode_hysteresis', 0.1)  # Prevent chattering in mode switching
    new_params.setdefault('transition_smoothing', True)  # Smooth mode transitions
    new_params.setdefault('surface_consistency_check', True)  # Validate surface compatibility

    # Validate hybrid mode switching stability
    if 'switching_criteria' in new_params:
        criteria = new_params['switching_criteria']
        error_thresh = criteria.get('error_threshold', 0.1)
        time_thresh = criteria.get('time_threshold', 2.0)

        # Check switching frequency to prevent chattering
        min_dwell_time = 0.1  # Minimum time in each mode
        if time_thresh < min_dwell_time:
            print(f"Warning: Short time threshold {time_thresh}s may cause mode chattering")

    return new_params

# Mathematical validation example
old_hybrid_config = {
    'gains': [18.0, 12.0, 10.0, 8.0],  # Surface gains
    'mode': 'CLASSICAL_ADAPTIVE',
    'sub_controller_gains': {
        'classical': [20.0, 15.0, 12.0, 8.0, 35.0, 5.0],
        'adaptive': [25.0, 18.0, 15.0, 10.0, 4.0]
    },
    'switch_threshold': 0.1,
    'max_force': 150.0
}

migrated_config = migrate_hybrid_smc_parameters_mathematical(old_hybrid_config)
print("Migrated Hybrid SMC config:", migrated_config)