# Example from: docs\configuration_schema_validation.md
# Index: 11
# Runnable: False
# Hash: 6cca008c

def validate_physics_controller_compatibility(physics_config: dict, controller_config: dict) -> bool:
    """Validate compatibility between physics and controller parameters."""

    physics = PhysicsConfig(**physics_config)

    # System natural frequency estimation
    g = physics.gravity
    l1 = physics.pendulum_length_1
    l2 = physics.pendulum_length_2

    # Approximate natural frequency for upright equilibrium
    omega_n1 = np.sqrt(g / l1)  # Pendulum 1
    omega_n2 = np.sqrt(g / l2)  # Pendulum 2

    if controller_config['type'] == 'classical_smc':
        gains = controller_config['gains']
        lambda1, lambda2 = gains[0], gains[1]

        # Sliding surface design rule: λᵢ ≈ 2ζωₙᵢ where ζ ≈ 0.7
        recommended_lambda1 = 2 * 0.7 * omega_n1
        recommended_lambda2 = 2 * 0.7 * omega_n2

        # Check if gains are reasonably close to recommendations
        if lambda1 < 0.1 * recommended_lambda1 or lambda1 > 10 * recommended_lambda1:
            raise ValueError(f"λ₁={lambda1} far from recommended {recommended_lambda1:.2f}")

        if lambda2 < 0.1 * recommended_lambda2 or lambda2 > 10 * recommended_lambda2:
            raise ValueError(f"λ₂={lambda2} far from recommended {recommended_lambda2:.2f}")

    return True