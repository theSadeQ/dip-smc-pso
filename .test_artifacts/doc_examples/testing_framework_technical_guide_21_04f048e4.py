# Example from: docs\testing\testing_framework_technical_guide.md
# Index: 21
# Runnable: False
# Hash: 04f048e4

# tests/utils/generators.py

def generate_initial_conditions(n_samples=100, max_deviation=0.2):
    """Generate random initial conditions for robustness testing."""
    return np.random.uniform(
        -max_deviation,
        max_deviation,
        size=(n_samples, 6)
    )

def generate_physics_variations(base_params, uncertainty=0.1, n_samples=50):
    """Generate physics parameter variations for robustness testing."""
    variations = []
    for _ in range(n_samples):
        varied = {}
        for param, value in base_params.items():
            if isinstance(value, (int, float)):
                variation = value * (1 + np.random.uniform(-uncertainty, uncertainty))
                varied[param] = variation
            else:
                varied[param] = value
        variations.append(varied)
    return variations

def generate_disturbance_profiles(duration, dt, disturbance_types=['impulse', 'step', 'ramp']):
    """Generate disturbance profiles for testing."""
    profiles = {}

    t = np.arange(0, duration, dt)

    for dist_type in disturbance_types:
        if dist_type == 'impulse':
            profile = np.zeros_like(t)
            impulse_index = len(t) // 2
            profile[impulse_index] = 50.0
        elif dist_type == 'step':
            profile = np.where(t > duration/2, 20.0, 0.0)
        elif dist_type == 'ramp':
            profile = 10.0 * t / duration

        profiles[dist_type] = profile

    return profiles