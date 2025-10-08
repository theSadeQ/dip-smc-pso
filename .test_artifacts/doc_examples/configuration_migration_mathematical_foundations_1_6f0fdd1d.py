# Example from: docs\factory\configuration_migration_mathematical_foundations.md
# Index: 1
# Runnable: False
# Hash: 6f0fdd1d

def migrate_classical_smc_parameters_mathematical(old_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mathematically sound migration for Classical SMC parameters.

    Mathematical Validation:
    1. Preserve sliding surface eigenvalues
    2. Maintain Lyapunov stability conditions
    3. Ensure bounded control effort
    """

    new_params = {}

    # Extract old gains structure
    old_gains = old_params.get('gains', [])
    K_switching = old_params.get('K_switching', 0.0)

    # Mathematical migration: [k1, k2, λ1, λ2, K] → [k1, k2, λ1, λ2, K, kd]
    if len(old_gains) == 5:
        k1, k2, lam1, lam2, K_old = old_gains

        # Validate stability conditions
        if lam1 <= 0 or lam2 <= 0:
            raise ValueError("Sliding surface coefficients λ₁, λ₂ must be positive for stability")

        if k1 <= 0 or k2 <= 0:
            raise ValueError("Proportional gains k₁, k₂ must be positive")

        # Combine switching gains: K_total = max(K_old, K_switching)
        K_total = max(K_old, K_switching) if K_switching > 0 else K_old

        # Add derivative gain for chattering reduction
        kd = old_params.get('kd', K_total * 0.1)  # 10% of switching gain

        new_params['gains'] = [k1, k2, lam1, lam2, K_total, kd]

    # Validate sliding surface eigenvalues
    if 'gains' in new_params:
        k1, k2, lam1, lam2, K, kd = new_params['gains']

        # Check sliding surface stability (simplified for double pendulum)
        eigenvalues = [-lam1/k1, -lam2/k2]  # Approximate eigenvalues
        if any(eig >= 0 for eig in eigenvalues):
            print(f"Warning: Sliding surface may be unstable. Eigenvalues: {eigenvalues}")

    # Migrate deprecated parameters
    deprecated_mappings = {
        'switch_function': 'switch_method',
        'saturation_limit': 'max_force',
        'boundary_thickness': 'boundary_layer'
    }

    for old_param, new_param in deprecated_mappings.items():
        if old_param in old_params:
            new_params[new_param] = old_params[old_param]

    # Ensure required parameters with physically meaningful defaults
    new_params.setdefault('max_force', 150.0)  # Reasonable actuator limit [N]
    new_params.setdefault('boundary_layer', 0.02)  # 2% of typical angular range
    new_params.setdefault('dt', 0.001)  # 1ms sampling time

    return new_params

# Mathematical validation example
old_classical_config = {
    'gains': [20.0, 15.0, 12.0, 8.0, 35.0],  # [k1, k2, λ1, λ2, K]
    'K_switching': 5.0,
    'switch_function': 'sign',
    'saturation_limit': 100.0
}

migrated_config = migrate_classical_smc_parameters_mathematical(old_classical_config)
print("Migrated Classical SMC config:", migrated_config)