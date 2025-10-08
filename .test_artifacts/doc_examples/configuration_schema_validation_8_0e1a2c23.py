# Example from: docs\configuration_schema_validation.md
# Index: 8
# Runnable: False
# Hash: 0e1a2c23

def validate_lyapunov_stability_constraints(controller_config: dict, physics_config: dict) -> bool:
    """Validate Lyapunov stability mathematical constraints."""

    if controller_config['type'] == 'classical_smc':
        gains = controller_config['gains']
        lambda1, lambda2 = gains[0], gains[1]

        # Stability requirement: λᵢ > 0
        if lambda1 <= 0 or lambda2 <= 0:
            raise ValueError("Sliding surface gains must be positive for stability")

        # Convergence rate constraints
        if lambda1 < 0.5 or lambda2 < 0.5:
            raise ValueError("Sliding surface gains too small, slow convergence")

        if lambda1 > 50.0 or lambda2 > 50.0:
            raise ValueError("Sliding surface gains too large, excessive control effort")

        # Relative stability margins
        physics = PhysicsConfig(**physics_config)
        system_inertia = physics.cart_mass + physics.pendulum_mass_1 + physics.pendulum_mass_2

        max_stable_gain = 100 / system_inertia  # Heuristic stability bound
        if max(gains) > max_stable_gain:
            raise ValueError(f"Control gains exceed stability bound for system inertia")

    return True