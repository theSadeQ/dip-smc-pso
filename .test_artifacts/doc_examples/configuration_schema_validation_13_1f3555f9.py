# Example from: docs\configuration_schema_validation.md
# Index: 13
# Runnable: False
# Hash: 1f3555f9

# example-metadata:
# runnable: false

def validate_simulation_system_compatibility(sim_config: dict, physics_config: dict) -> bool:
    """Validate simulation parameters with physical system."""

    physics = PhysicsConfig(**physics_config)
    sim = SimulationConfig(**sim_config)

    # Time scale compatibility
    g = physics.gravity
    l_min = min(physics.pendulum_length_1, physics.pendulum_length_2)
    time_scale = np.sqrt(l_min / g)  # Natural time scale

    if sim.dt > 0.1 * time_scale:
        raise ValueError(f"Time step too large compared to system time scale {time_scale:.3f}s")

    # Initial condition feasibility
    theta1, theta2, x = sim.initial_state[:3]

    # Physical constraints (pendulums can't overlap with cart)
    l1, l2 = physics.pendulum_length_1, physics.pendulum_length_2

    # Simplified collision check for extreme angles
    if abs(theta1) > np.pi/3 and abs(theta2) > np.pi/3:
        # Check potential collision (simplified)
        x1_end = x + l1 * np.sin(theta1)
        x2_end = x + l2 * np.sin(theta2)
        if abs(x1_end - x2_end) < 0.1:  # 10cm clearance
            raise ValueError("Initial configuration may cause pendulum collision")

    return True