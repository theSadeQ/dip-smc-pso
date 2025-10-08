# Example from: docs\configuration_schema_validation.md
# Index: 12
# Runnable: False
# Hash: 7dddfa26

# example-metadata:
# runnable: false

def validate_optimization_controller_compatibility(opt_config: dict, ctrl_configs: dict) -> bool:
    """Validate optimization bounds with controller requirements."""

    if 'pso' not in opt_config:
        return True

    pso_config = opt_config['pso']

    for controller_name, controller_config in ctrl_configs.items():
        if controller_name not in pso_config['bounds']:
            continue

        bounds = pso_config['bounds'][controller_name]

        if controller_name == 'classical_smc':
            # Validate bounds for stability requirements
            lambda1_bounds = bounds[0]  # [min, max] for λ₁
            lambda2_bounds = bounds[1]  # [min, max] for λ₂

            if lambda1_bounds[0] <= 0 or lambda2_bounds[0] <= 0:
                raise ValueError("SMC gain lower bounds must be positive")

            # Current gains should be within optimization bounds
            current_gains = controller_config.get('gains', [])
            for i, (current_gain, bound_pair) in enumerate(zip(current_gains, bounds)):
                if not bound_pair[0] <= current_gain <= bound_pair[1]:
                    raise ValueError(f"Current gain {i} outside optimization bounds")

    return True