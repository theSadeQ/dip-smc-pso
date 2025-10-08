# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 18
# Runnable: False
# Hash: 69667a9c

# example-metadata:
# runnable: false

# Automatic test scenarios in fitness evaluation:
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
        'weight': 1.5,
        'description': 'large_angles'
    },
    {
        'initial_state': [0.0, 0.2, 0.1, 0.0, 1.0, 0.5],   # High velocity
        'sim_time': 2.5,
        'weight': 1.2,
        'description': 'high_velocity'
    }
]