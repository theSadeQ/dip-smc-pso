# Example from: docs\technical\factory_integration_fixes_issue6.md
# Index: 38
# Runnable: True
# Hash: 33bdb6ce

# Simple dict-based configuration - still works
config = {
    'gains': [8.0, 6.0, 4.0, 3.0, 15.0, 2.0],
    'max_force': 150.0,
    'boundary_layer': 0.02
}

controller = create_controller('classical_smc', config=config)