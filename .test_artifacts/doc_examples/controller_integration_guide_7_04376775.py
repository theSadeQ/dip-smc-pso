# Example from: docs\factory\controller_integration_guide.md
# Index: 7
# Runnable: True
# Hash: 04376775

# Pattern 1: Simplified DIP Configuration
def create_simplified_plant_config():
    """Create simplified DIP plant configuration for rapid prototyping."""
    from src.plant.configurations import ConfigurationFactory

    config = ConfigurationFactory.create_default_config("simplified")
    return {
        'dynamics_type': 'simplified',
        'config': config,
        'linearization_point': np.zeros(6),
        'use_cases': ['controller_tuning', 'pso_optimization', 'rapid_testing']
    }

# Pattern 2: Full Nonlinear DIP Configuration
def create_full_nonlinear_plant_config():
    """Create full nonlinear DIP configuration for high-fidelity simulation."""
    from src.plant.configurations import ConfigurationFactory

    config = ConfigurationFactory.create_default_config("full")
    return {
        'dynamics_type': 'full_nonlinear',
        'config': config,
        'friction_models': ['viscous', 'coulomb'],
        'disturbance_rejection': True,
        'use_cases': ['performance_validation', 'robustness_testing', 'real_system_prep']
    }

# Pattern 3: HIL-Ready Configuration
def create_hil_plant_config():
    """Create HIL-compatible plant configuration."""
    config = create_full_nonlinear_plant_config()
    config.update({
        'real_time_constraints': True,
        'communication_interface': 'tcp_socket',
        'sampling_rate': 1000,  # 1 kHz for real-time control
        'latency_compensation': True,
        'safety_monitors': ['position_limits', 'velocity_limits', 'control_limits']
    })
    return config