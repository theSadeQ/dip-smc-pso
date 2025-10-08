# Example from: docs\technical\pso_integration_workflows.md
# Index: 11
# Runnable: False
# Hash: 79d20a58

# Automatic test scenarios (built into enhanced fitness function):
test_scenarios = [
    {
        'initial_state': [0.0, 0.1, 0.05, 0.0, 0.0, 0.0],  # Small disturbance
        'sim_time': 2.0,
        'weight': 1.0,
        'description': 'small_disturbance'
    },
    {
        'initial_state': [0.0, 0.5, 0.3, 0.0, 0.0, 0.0],   # Large angles
        'sim_time': 3.0,
        'weight': 1.5,     # Higher weight for challenging scenario
        'description': 'large_angles'
    },
    {
        'initial_state': [0.0, 0.2, 0.1, 0.0, 1.0, 0.5],   # High velocity
        'sim_time': 2.5,
        'weight': 1.2,
        'description': 'high_velocity'
    }
]