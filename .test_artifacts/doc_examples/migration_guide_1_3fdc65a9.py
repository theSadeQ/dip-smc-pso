# Example from: docs\factory\migration_guide.md
# Index: 1
# Runnable: False
# Hash: 3fdc65a9

# example-metadata:
# runnable: false

# Pre-Migration Configuration (v1.x)
old_config = {
    'classical_smc': {
        'gains': [10, 5, 8, 3, 15],     # 5 gains instead of 6
        'K_switching': 2.0,              # Separate switching gain
        'gamma': 0.1,                    # Invalid for classical SMC
        'switch_function': 'sign'        # Old parameter name
    },
    'adaptive_smc': {
        'gains': [12, 10, 6, 5],        # 4 gains instead of 5
        'adaptation_gain': 2.5,          # Separate adaptation gain
        'boundary_layer_thickness': 0.02, # Old parameter name
        'estimate_bounds': [0.1, 100.0]  # Old format
    }
}

# Post-Migration Configuration (v2.x+)
new_config = {
    'classical_smc': {
        'gains': [10, 5, 8, 3, 15, 2.0], # 6 gains with K included
        'boundary_layer': 0.02,          # Correct parameter
        'switch_method': 'sign'          # New parameter name
    },
    'adaptive_smc': {
        'gains': [12, 10, 6, 5, 2.5],   # 5 gains with gamma included
        'boundary_layer': 0.02,          # Renamed parameter
        'K_min': 0.1,                    # Split parameter
        'K_max': 100.0                   # Split parameter
    }
}