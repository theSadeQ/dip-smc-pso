# Example from: docs\factory\factory_integration_user_guide.md
# Index: 6
# Runnable: False
# Hash: 3d46b50f

adaptive_config = {
    'gains': [25.0, 18.0, 15.0, 10.0, 4.0],
    'max_force': 150.0,
    'dt': 0.001,
    'leak_rate': 0.01,
    'adapt_rate_limit': 10.0,
    'K_min': 0.1,
    'K_max': 100.0,
    'alpha': 0.5
}

controller = create_controller('adaptive_smc', **adaptive_config)